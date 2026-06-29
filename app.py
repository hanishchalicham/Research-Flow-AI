from __future__ import annotations

import asyncio
from pathlib import Path
import streamlit as st

from config.settings import APP_NAME, require_api_key
from agents.orchestrator import run_research_workflow
from tools.memory import list_recent_memory
from tools.visuals import workflow_mermaid, confidence_badge

st.set_page_config(page_title=APP_NAME, page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.title("🧠 ResearchFlow AI")
st.caption("A portfolio-ready multi-agent research platform with planning, evidence validation, reporting, and exports.")

if not require_api_key():
    st.error("OPENAI_API_KEY is missing. Copy .env.example to .env and add your API key.")
    st.stop()

with st.sidebar:
    st.header("Research Console")
    topic = st.text_area(
        "Research topic",
        placeholder="Example: How are AI agents changing enterprise data analytics?",
        height=110,
    )
    start = st.button("Start Research", type="primary", disabled=not topic.strip())

    st.divider()
    st.subheader("Example Topics")
    examples = [
        "How are multi-agent AI systems improving enterprise analytics workflows?",
        "What are the risks and benefits of retrieval augmented generation in healthcare?",
        "How can OpenTelemetry improve observability for AI-powered applications?",
    ]
    for ex in examples:
        if st.button(ex):
            topic = ex
            start = True

    st.divider()
    st.subheader("Recent Memory")
    recent = list_recent_memory()
    if recent:
        for item in recent:
            st.caption(f"{item['topic']} — {item['saved_at'][:10]}")
    else:
        st.caption("No saved research yet.")

tab_overview, tab_process, tab_report, tab_sources = st.tabs(["Overview", "Process", "Report", "Evidence"])

with tab_overview:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("Workflow")
        st.markdown(workflow_mermaid())
    with col2:
        st.subheader("What this project demonstrates")
        st.markdown(
            """
            - Multi-agent orchestration with OpenAI Agents SDK
            - Structured outputs with Pydantic models
            - Evidence capture and validation
            - Markdown/PDF report export
            - Research memory for reproducibility
            - Recruiter-friendly Streamlit dashboard
            """
        )

if "result" not in st.session_state:
    st.session_state.result = None

if start:
    with tab_process:
        st.info("Running the full research workflow: plan → search → validate → report → export.")
        progress = st.progress(0)
        status = st.empty()
        try:
            status.write("Planning research...")
            progress.progress(15)
            result = asyncio.run(run_research_workflow(topic.strip()))
            progress.progress(100)
            status.success("Research completed successfully.")
            st.session_state.result = result
        except Exception as exc:
            st.error(f"Workflow failed: {exc}")

result = st.session_state.result

with tab_process:
    if result:
        st.subheader("Research Plan")
        st.json(result["plan"].model_dump())
        st.subheader("Validation Summary")
        st.json(result["validation"].model_dump())
    else:
        st.caption("Start a research run to see the live process.")

with tab_report:
    if result:
        report = result["report"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Confidence", f"{report.confidence_score}%", confidence_badge(report.confidence_score))
        col2.metric("Word Count", report.word_count)
        col3.metric("Sources", len(report.sources))

        st.markdown(report.markdown_report)

        md_path = Path(result["markdown_path"])
        pdf_path = Path(result["pdf_path"])
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button("Download Markdown", md_path.read_bytes(), file_name=md_path.name, mime="text/markdown")
        with col_b:
            st.download_button("Download PDF", pdf_path.read_bytes(), file_name=pdf_path.name, mime="application/pdf")
    else:
        st.caption("Your generated research report will appear here.")

with tab_sources:
    if result:
        st.subheader("Captured Evidence")
        evidence = result["evidence"]
        if evidence:
            for item in evidence:
                st.info(f"**Claim:** {item.claim}\n\n**Source:** {item.source}\n\n**Confidence:** {item.confidence}%")
        else:
            st.warning("No evidence was captured by the tool. The report may still contain model-generated notes.")

        st.subheader("Sources from Final Report")
        for src in result["report"].sources:
            st.write(src)
    else:
        st.caption("Evidence and sources will appear after a run.")
