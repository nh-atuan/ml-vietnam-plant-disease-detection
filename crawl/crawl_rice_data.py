import argparse
import asyncio
import base64
import json
import uuid
from pathlib import Path

import httpx
from crawl4ai import AsyncWebCrawler
from ddgs import DDGS
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm

MAX_CONCURRENT_SCRAPES = 5
MAX_CONCURRENT_AI = 2


def search_with_serper(query: str, api_key: str) -> list:
    """Perform a search using Serper.dev API."""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    try:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, data=payload, timeout=15.0)
            response.raise_for_status()
            results = response.json().get("organic", [])
            return [r.get("link") for r in results if r.get("link")]
    except Exception as e:
        print(f"Error searching with Serper for query '{query}': {e}")
        return []


def generate_target_urls(args):
    """Find target URLs using expanded query strategies via chosen search engine."""
    search_strategy = {
        "BrownSpot": [
            "Bệnh đốm nâu hại lúa site:.vn",
            "triệu chứng đốm nâu lúa site:.vn",
            "hình ảnh bệnh đốm nâu lúa site:.vn",
        ],
        "LeafBlast": ["Bệnh đạo ôn hại lúa site:.vn", "bệnh đạo ôn lúa site:.vn", "hình ảnh bệnh đạo ôn lúa site:.vn"],
        "Hispa": ["Bọ gai hại lúa site:.vn", "hình ảnh bọ gai lúa site:.vn"],
        "Healthy": ["Lúa khỏe mạnh site:.vn", "cây lúa phát triển tốt site:.vn"],
    }

    all_urls = set()
    print(f"Starting automated search for agricultural URLs using {args.search_engine.upper()}...")

    if args.search_engine == "serper" and not args.serper_api_key:
        raise ValueError("Serper API key is required when using the 'serper' search engine.")

    # DuckDuckGo logic
    if args.search_engine == "ddg":
        with DDGS() as ddgs:
            for label, queries in search_strategy.items():
                for query in queries:
                    print(f"--> Searching: {query}")
                    try:
                        results = ddgs.text(query, max_results=50)
                        for r in results:
                            url = r.get("href")
                            if url:
                                all_urls.add(url)
                    except Exception as e:
                        print(f"Error searching for {label} with query {query}: {e}")

    # Serper.dev logic
    elif args.search_engine == "serper":
        for label, queries in search_strategy.items():
            for query in queries:
                print(f"--> Searching: {query}")
                urls = search_with_serper(query, args.serper_api_key)
                all_urls.update(urls)

    print(f"\nSuccessfully found {len(all_urls)} unique URLs.")
    return list(all_urls)


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


async def classify_image(base64_image: str, context: str, client: AsyncOpenAI) -> str:
    """Asks the local VLM to classify the image and context."""
    prompt_text = f"""You are an agricultural expert. Look at this image and the surrounding text from a Vietnamese blog: "{context}".
    Determine if this is a valid close-up of a rice plant. If it is, classify it strictly as ONE of these four categories: Healthy, BrownSpot, Hispa, or LeafBlast.
    Respond ONLY with a JSON object in this format: {{"prediction": "LabelName"}}. If it is not a valid image of a rice plant, respond with {{"prediction": "Invalid"}}."""
    try:
        response = await client.chat.completions.create(
            model="Gemma 4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": base64_image}},
                    ],
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        ai_output = response.choices[0].message.content
        prediction_data = json.loads(ai_output)
        return prediction_data.get("prediction", "Unknown")
    except Exception as e:
        return f"Error: {e}"


async def scrape_url(url, crawler, http_client, args, semaphore, pending_file, processed_log, file_lock):
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

                img_save_path = Path(args.output_dir) / "images" / img_filename
                txt_save_path = Path(args.output_dir) / "context" / txt_filename
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


async def classify_task(task_data, ai_client, args, semaphore, final_file, file_lock):
    """Reads a single task from the pending file, classifies it, and saves securely."""
    async with semaphore:
        try:
            predicted_label = await classify_image(task_data["base64"], task_data["context"], ai_client)

            ls_task = {
                "data": {
                    "image": task_data["image_path"],
                    "context": task_data["context"],
                    "source_url": task_data["source_url"],
                    "local_txt": task_data["local_txt"],
                }
            }

            if predicted_label in ["Healthy", "BrownSpot", "Hispa", "LeafBlast"]:
                ls_task["predictions"] = [
                    {
                        "model_version": "Gemma 4",
                        "result": [
                            {
                                "from_name": "choice",
                                "to_name": "image",
                                "type": "choices",
                                "value": {"choices": [predicted_label]},
                            }
                        ],
                    }
                ]

            async with file_lock:
                with open(final_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(ls_task, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"  [!] Error classifying image {task_data['image_path']}: {e}")


async def main_pipeline(args):
    """Pipeline Orchestration"""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pending_file = Path(args.output_dir) / "pending_images.jsonl"
    final_file = Path(args.import_file)
    processed_log = Path(args.output_dir) / "processed_urls.txt"
    file_lock = asyncio.Lock()

    # 1. SCRAPING PHASE
    print("\n PHASE 1: SCRAPING & DOWNLOADING ")
    processed_urls = set()
    if processed_log.exists():
        processed_urls = set(processed_log.read_text(encoding="utf-8").splitlines())

    all_urls = generate_target_urls(args)
    urls_to_process = [u for u in all_urls if u not in processed_urls]

    if urls_to_process:
        async with AsyncWebCrawler(verbose=False) as crawler:
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                scrape_sem = asyncio.Semaphore(MAX_CONCURRENT_SCRAPES)

                scrape_tasks = [
                    scrape_url(url, crawler, http_client, args, scrape_sem, pending_file, processed_log, file_lock)
                    for url in urls_to_process
                ]

                for f in tqdm(asyncio.as_completed(scrape_tasks), total=len(scrape_tasks), desc="Scraping"):
                    await f
    else:
        print("No new URLs to scrape.")

    # 2. CLASSIFICATION PHASE
    print("\n PHASE 2: AI CLASSIFICATION (Gemma 4) ")
    if not pending_file.exists():
        print("No pending images found. Skipping classification.")
        return

    # Track already classified images to resume classification properly
    processed_images = set()
    if final_file.exists():
        with open(final_file, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        processed_images.add(record["data"]["image"])
                    except json.JSONDecodeError:
                        pass

    # Read pending tasks and filter out already processed ones
    pending_tasks = []
    with open(pending_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                task = json.loads(line)
                if task.get("image_path") not in processed_images:
                    pending_tasks.append(task)

    if pending_tasks:
        ai_client = AsyncOpenAI(
            base_url=args.base_url,
            api_key=args.api_key,
            http_client=httpx.AsyncClient(headers={"ngrok-skip-browser-warning": "true"}),
        )
        ai_sem = asyncio.Semaphore(MAX_CONCURRENT_AI)

        classify_tasks = [classify_task(task, ai_client, args, ai_sem, final_file, file_lock) for task in pending_tasks]

        for f in tqdm(asyncio.as_completed(classify_tasks), total=len(classify_tasks), desc="Classifying"):
            await f

        pending_file.unlink(missing_ok=True)
    else:
        print("All pending images have already been classified.")

    print(f"\nPipeline Complete! Data saved to {final_file}")
    convert_jsonl_to_json(final_file, final_file.parent / f"{final_file.stem}.json")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search-engine",
        type=str,
        choices=["ddg", "serper"],
        default="ddg",
        help="Search engine to use (ddg or serper)",
    )
    parser.add_argument("--serper-api-key", type=str, default="", help="API key for Serper.dev")
    parser.add_argument("--output-dir", type=str, default="datasets/raw/scraped_data")
    parser.add_argument("--base-url", type=str, default="http://localhost:8080/v1")
    parser.add_argument("--api-key", type=str, default="sk-no-key-needed")
    parser.add_argument("--import-file", type=str, default="datasets/raw/label_studio_import.jsonl")
    parser.add_argument("--max_concurrent_scrapes", type=int, default=5)
    parser.add_argument("--max_concurrent_ai", type=int, default=2)

    args = parser.parse_args()

    if args.max_concurrent_scrapes != MAX_CONCURRENT_SCRAPES:
        MAX_CONCURRENT_SCRAPES = args.max_concurrent_scrapes
    if args.max_concurrent_ai != MAX_CONCURRENT_AI:
        MAX_CONCURRENT_AI = args.max_concurrent_ai

    asyncio.run(main_pipeline(args))
