from __future__ import annotations

from agents import Agent, WebSearchTool
from config.settings import OPENAI_MODEL

academic_agent = Agent(
    name="Academic Lens Agent",
    model=OPENAI_MODEL,
    tools=[WebSearchTool()],
    instructions=(
        "You are an academic research reviewer. Look for scholarly, technical, standards-based, "
        "or evidence-heavy context related to the topic. Identify frameworks, datasets, methods, "
        "limitations, and open questions. Keep output under 500 words and cite source names or links."
    ),
)
