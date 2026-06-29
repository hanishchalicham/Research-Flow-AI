from __future__ import annotations

import argparse
import asyncio
from config.settings import require_api_key
from agents.orchestrator import run_research_workflow


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run ResearchFlow AI from the command line.")
    parser.add_argument("topic", help="Research topic to investigate")
    args = parser.parse_args()

    if not require_api_key():
        raise RuntimeError("OPENAI_API_KEY is missing. Create .env from .env.example.")

    result = await run_research_workflow(args.topic)
    print("Research complete")
    print(f"Markdown: {result['markdown_path']}")
    print(f"PDF: {result['pdf_path']}")
    print(f"Memory: {result['memory_path']}")


if __name__ == "__main__":
    asyncio.run(main())
