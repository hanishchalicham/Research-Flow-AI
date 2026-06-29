from __future__ import annotations


def workflow_mermaid() -> str:
    return """```mermaid
graph TD
    A[User Research Topic] --> B[Planning Agent]
    B --> C[Web Research Agent]
    B --> D[Academic Lens Agent]
    C --> E[Evidence Validator]
    D --> E
    E --> F[Report Writer]
    F --> G[Markdown/PDF Export]
    F --> H[Research Memory]
```"""


def confidence_badge(score: int) -> str:
    if score >= 85:
        return "High"
    if score >= 65:
        return "Medium"
    return "Needs Review"
