from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "ResearchFlow AI")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EDITOR_MODEL = os.getenv("OPENAI_EDITOR_MODEL", OPENAI_MODEL)
REPORT_OUTPUT_DIR = Path(os.getenv("REPORT_OUTPUT_DIR", "reports"))
MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "memory/history"))

REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def require_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))
