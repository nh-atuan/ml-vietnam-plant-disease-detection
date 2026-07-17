import base64
import json
import uuid
from pathlib import Path

import httpx


def convert_jsonl_to_json(input_file: Path, output_file: Path):
    if not input_file.exists():
        return
    data = []
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Converted {len(data)} items to {output_file}")


async def fetch_image_data(url: str, http_client: httpx.AsyncClient):
    """Downloads an image and returns bytes, mime_type, and base64 string."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = await http_client.get(url, headers=headers, timeout=15.0, follow_redirects=True)
        response.raise_for_status()
        img_bytes = response.content

        mime_type = "image/jpeg"
        if url.lower().endswith(".png"):
            mime_type = "image/png"
        elif url.lower().endswith(".webp"):
            mime_type = "image/webp"

        b64_string = f"data:{mime_type};base64,{base64.b64encode(img_bytes).decode('utf-8')}"
        return img_bytes, mime_type, b64_string
    except Exception:
        return None, None, None


async def scrape_url(url, label, crawler, http_client, args, semaphore, pending_file, processed_log, file_lock):
    """Crawls a URL, saves images/context to disk, and marks URL as processed securely."""
    async with semaphore:
        tasks_to_add = []
        try:
            result = await crawler.arun(url=url)
            if not result.success or not result.media.get("images"):
                return

            for img in result.media["images"]:
                img_url = img.get("src")
                if not img_url or img_url.endswith((".svg", ".gif", ".ico")):
                    continue

                context_text = (img.get("alt") or "") + " " + (img.get("desc") or "")
                context_text = context_text.strip()

                img_bytes, mime_type, base64_image = await fetch_image_data(img_url, http_client)
                if not base64_image:
                    continue

                unique_id = str(uuid.uuid4())[:8]
                img_filename = f"img_{unique_id}.{mime_type.split('/')[-1]}"
                txt_filename = f"text_{unique_id}.txt"

                img_save_path = Path(args.output_dir) / "images" / label / img_filename
                txt_save_path = Path(args.output_dir) / "context" / label / txt_filename
                img_save_path.parent.mkdir(parents=True, exist_ok=True)
                txt_save_path.parent.mkdir(parents=True, exist_ok=True)

                with open(img_save_path, "wb") as f:
                    f.write(img_bytes)
                with open(txt_save_path, "w", encoding="utf-8") as f:
                    f.write(f"Source: {url}\nContext: {context_text}")

                task_metadata = {
                    "image_path": str(img_save_path.absolute()),
                    "context": context_text,
                    "source_url": url,
                    "local_txt": str(txt_save_path.absolute()),
                    "base64": base64_image,
                }
                tasks_to_add.append(task_metadata)

            if tasks_to_add:
                async with file_lock:
                    with open(pending_file, "a", encoding="utf-8") as f:
                        for t in tasks_to_add:
                            f.write(json.dumps(t, ensure_ascii=False) + "\n")

        except Exception as e:
            print(f"  [!] Error scraping {url}: {e}")
        finally:
            # Save progress incrementally to prevent data loss if interrupted
            async with file_lock:
                with open(processed_log, "a", encoding="utf-8") as f:
                    f.write(url + "\n")
