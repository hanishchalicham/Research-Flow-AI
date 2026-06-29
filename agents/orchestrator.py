from __future__ import annotations

from datetime import datetime
from pathlib import Path
from agents import Runner, trace

from agents.planner import planner_agent
from agents.web_research import web_research_agent, reset_evidence, get_evidence
from agents.academic import academic_agent
from agents.validator import validator_agent
from agents.report_writer import report_writer_agent
from config.settings import REPORT_OUTPUT_DIR
from models import ResearchPlan, ValidationSummary, ResearchReport
from tools.exporters import save_markdown, save_pdf_from_markdown
from tools.memory import save_report_memory


async def run_research_workflow(topic: str) -> dict:
    """Run the full ResearchFlow AI workflow and return all artifacts."""
    reset_evidence()
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    with trace("ResearchFlow AI", group_id=run_id):
        plan_result = await Runner.run(planner_agent, f"Create a research plan for: {topic}")
        plan: ResearchPlan = plan_result.final_output

        research_prompt = (
            f"Topic: {plan.topic}\nObjective: {plan.objective}\n"
            f"Search queries: {plan.search_queries}\nFocus areas: {plan.focus_areas}\n"
            "Research each focus area and capture important evidence."
        )
        web_result = await Runner.run(web_research_agent, research_prompt)
        academic_result = await Runner.run(academic_agent, research_prompt)
        evidence = get_evidence()

        validation_prompt = (
            f"Original topic: {topic}\n\nPlan:\n{plan.model_dump()}\n\n"
            f"Web notes:\n{web_result.final_output}\n\nAcademic notes:\n{academic_result.final_output}\n\n"
            f"Captured evidence:\n{[e.model_dump() for e in evidence]}"
        )
        validation_result = await Runner.run(validator_agent, validation_prompt)
        validation: ValidationSummary = validation_result.final_output

        report_prompt = (
            f"Write the final research report.\n\nTopic: {topic}\n\n"
            f"Research plan: {plan.model_dump()}\n\n"
            f"Web research notes: {web_result.final_output}\n\n"
            f"Academic notes: {academic_result.final_output}\n\n"
            f"Evidence: {[e.model_dump() for e in evidence]}\n\n"
            f"Validation: {validation.model_dump()}"
        )
        report_result = await Runner.run(report_writer_agent, report_prompt)
        report: ResearchReport = report_result.final_output

    safe_name = "".join(c if c.isalnum() else "_" for c in topic.lower()).strip("_")[:60] or "research"
    md_path = REPORT_OUTPUT_DIR / f"{run_id}_{safe_name}.md"
    pdf_path = REPORT_OUTPUT_DIR / f"{run_id}_{safe_name}.pdf"
    save_markdown(report.markdown_report, md_path)
    save_pdf_from_markdown(report.markdown_report, pdf_path)
    memory_path = save_report_memory(topic, report, evidence)

    return {
        "run_id": run_id,
        "plan": plan,
        "web_notes": web_result.final_output,
        "academic_notes": academic_result.final_output,
        "evidence": evidence,
        "validation": validation,
        "report": report,
        "markdown_path": str(md_path),
        "pdf_path": str(pdf_path),
        "memory_path": str(memory_path),
    }
