from __future__ import annotations

from agents import Agent
from config.settings import OPENAI_MODEL
from models import ResearchPlan

planner_agent = Agent(
    name="Planning Agent",
    model=OPENAI_MODEL,
    output_type=ResearchPlan,
    instructions=(
        "You are a research strategist. Convert a user's topic into a practical research plan. "
        "Return a concise structured plan with an objective, 4-6 targeted search queries, "
        "3-5 focus areas, and expected outputs. Avoid generic wording."
    ),
)
