import argparse


def parse_args():
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
    parser.add_argument("--max_concurrent_ai", type=int, default=4)

    args = parser.parse_args()
    return args
