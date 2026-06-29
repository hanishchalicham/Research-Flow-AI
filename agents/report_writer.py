from __future__ import annotations

from agents import Agent
from config.settings import OPENAI_EDITOR_MODEL
from models import ResearchReport

report_writer_agent = Agent(
    name="Report Writer",
    model=OPENAI_EDITOR_MODEL,
    output_type=ResearchReport,
    instructions=(
        "You are a senior research editor. Create a polished markdown research report. "
        "Structure it with title, executive summary, background, key findings, analysis, limitations, "
        "recommendations, conclusion, and sources. Use clear citations when source names or URLs are supplied. "
        "Do not fabricate sources. Include a confidence score based on evidence quality."
    ),
)
