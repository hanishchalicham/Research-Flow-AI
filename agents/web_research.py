from __future__ import annotations

from agents import Agent, WebSearchTool, function_tool
from config.settings import OPENAI_MODEL
from models import EvidenceItem

_collected_evidence: list[EvidenceItem] = []


@function_tool
def capture_evidence(claim: str, source: str = "Not specified", source_type: str = "web", confidence: int = 70) -> str:
    """Capture a research claim with its source and confidence score."""
    confidence = max(0, min(100, int(confidence)))
    item = EvidenceItem(claim=claim, source=source, source_type=source_type, confidence=confidence)
    _collected_evidence.append(item)
    return f"Evidence captured: {claim}"


def reset_evidence() -> None:
    _collected_evidence.clear()


def get_evidence() -> list[EvidenceItem]:
    return list(_collected_evidence)


web_research_agent = Agent(
    name="Web Research Agent",
    model=OPENAI_MODEL,
    tools=[WebSearchTool(), capture_evidence],
    instructions=(
        "You are a precise web research specialist. Search for current, credible information. "
        "Summarize only the most relevant findings. For each important claim, call capture_evidence "
        "with the claim, source URL or publication name, source type, and confidence. "
        "Prefer primary sources, official documentation, academic sources, and reputable publications."
    ),
)
