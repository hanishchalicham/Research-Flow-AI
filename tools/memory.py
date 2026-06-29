from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List

from config.settings import MEMORY_DIR
from models import EvidenceItem, ResearchReport


def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return cleaned[:80] or "research"


def save_report_memory(topic: str, report: ResearchReport, evidence: List[EvidenceItem]) -> Path:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "topic": topic,
        "saved_at": datetime.utcnow().isoformat(),
        "report": report.model_dump(),
        "evidence": [item.model_dump() for item in evidence],
    }
    path = MEMORY_DIR / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{_slugify(topic)}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def list_recent_memory(limit: int = 5) -> list[dict]:
    files = sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:limit]
    rows: list[dict] = []
    for file in files:
        try:
            payload = json.loads(file.read_text(encoding="utf-8"))
            rows.append({
                "topic": payload.get("topic", file.stem),
                "saved_at": payload.get("saved_at", ""),
                "file": str(file),
            })
        except Exception:
            continue
    return rows
