from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    topic: str = Field(..., description="Clear research topic")
    objective: str = Field(..., description="Purpose of the research")
    search_queries: List[str] = Field(default_factory=list, description="Targeted queries")
    focus_areas: List[str] = Field(default_factory=list, description="Key areas to investigate")
    expected_outputs: List[str] = Field(default_factory=list, description="Expected deliverables")


class EvidenceItem(BaseModel):
    claim: str
    source: str = "Not specified"
    source_type: str = "web"
    confidence: int = Field(default=70, ge=0, le=100)
    captured_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ValidationSummary(BaseModel):
    supported_claims: List[str] = Field(default_factory=list)
    weak_claims: List[str] = Field(default_factory=list)
    missing_sources: List[str] = Field(default_factory=list)
    overall_confidence: int = Field(default=70, ge=0, le=100)


class ResearchReport(BaseModel):
    title: str
    executive_summary: str
    key_findings: List[str] = Field(default_factory=list)
    markdown_report: str
    sources: List[str] = Field(default_factory=list)
    confidence_score: int = Field(default=70, ge=0, le=100)
    word_count: int = 0
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
