from __future__ import annotations

from agents import Agent
from config.settings import OPENAI_MODEL
from models import ValidationSummary

validator_agent = Agent(
    name="Evidence Validator",
    model=OPENAI_MODEL,
    output_type=ValidationSummary,
    instructions=(
        "You are an evidence validation analyst. Review the research notes and evidence. "
        "Classify claims as supported, weak, or missing sources. Produce an overall confidence score. "
        "Penalize unsupported claims, vague citations, single-source claims, and outdated sources."
    ),
)
