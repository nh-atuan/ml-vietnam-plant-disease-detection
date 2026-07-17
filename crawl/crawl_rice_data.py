import asyncio
import json
from pathlib import Path

import httpx
from crawl4ai import AsyncWebCrawler
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm

from .args import parse_args
from .search import generate_target_urls
from .utils import convert_jsonl_to_json, scrape_url

MAX_CONCURRENT_SCRAPES = 5
MAX_CONCURRENT_AI = 2


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

    # 1. Scraping
    print("\n Scraping & downloading...")
    processed_urls = set()
    if processed_log.exists():
        processed_urls = set(processed_log.read_text(encoding="utf-8").splitlines())

    search_strategy = {
        "BrownSpot": [
            "Bệnh đốm nâu hại lúa site",
            "triệu chứng đốm nâu lúa site",
            "hình ảnh bệnh đốm nâu lúa site",
        ],
        "LeafBlast": ["Bệnh đạo ôn hại lúa site", "bệnh đạo ôn lúa site", "hình ảnh bệnh đạo ôn lúa site"],
        "Hispa": ["Bọ gai hại lúa site", "hình ảnh bọ gai lúa site"],
        "Healthy": ["Lúa khỏe mạnh site", "cây lúa phát triển tốt site"],
    }
    all_urls = generate_target_urls(args, search_strategy)
    urls_to_process = {u: label for u, label in all_urls.items() if u not in processed_urls}

    if urls_to_process:
        async with AsyncWebCrawler(verbose=False) as crawler:
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                scrape_sem = asyncio.Semaphore(MAX_CONCURRENT_SCRAPES)

                scrape_tasks = [
                    scrape_url(
                        url, label, crawler, http_client, args, scrape_sem, pending_file, processed_log, file_lock
                    )
                    for url, label in urls_to_process.items()
                ]

                for f in tqdm(asyncio.as_completed(scrape_tasks), total=len(scrape_tasks), desc="Scraping"):
                    await f
    else:
        print("No new URLs to scrape.")

    # 2. Classification
    print("\n AI classification (Gemma 4)...")
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
        if args.api_key == "None":
            print("  [i] Skipping AI classification (key 'None'). Saving tasks for manual labeling.")
            async with file_lock:
                with open(final_file, "a", encoding="utf-8") as f:
                    for task_data in pending_tasks:
                        ls_task = {
                            "data": {
                                "image": task_data["image_path"],
                                "context": task_data["context"],
                                "source_url": task_data["source_url"],
                                "local_txt": task_data["local_txt"],
                            }
                        }
                        f.write(json.dumps(ls_task, ensure_ascii=False) + "\n")
        else:
            ai_client = AsyncOpenAI(
                base_url=args.base_url,
                api_key=args.api_key,
                http_client=httpx.AsyncClient(headers={"ngrok-skip-browser-warning": "true"}),
            )
            ai_sem = asyncio.Semaphore(MAX_CONCURRENT_AI)

            classify_tasks = [
                classify_task(task, ai_client, args, ai_sem, final_file, file_lock) for task in pending_tasks
            ]

            for f in tqdm(asyncio.as_completed(classify_tasks), total=len(classify_tasks), desc="Classifying"):
                await f

        pending_file.unlink(missing_ok=True)
    else:
        print("All pending images have already been classified.")

    print(f"\nPipeline Complete! Data saved to {final_file}")
    convert_jsonl_to_json(final_file, final_file.parent / f"{final_file.stem}.json")


if __name__ == "__main__":
    args = parse_args()

    if args.max_concurrent_scrapes != MAX_CONCURRENT_SCRAPES:
        MAX_CONCURRENT_SCRAPES = args.max_concurrent_scrapes
    if args.max_concurrent_ai != MAX_CONCURRENT_AI:
        MAX_CONCURRENT_AI = args.max_concurrent_ai

    asyncio.run(main_pipeline(args))
