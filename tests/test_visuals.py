from tools.visuals import confidence_badge, workflow_mermaid


def test_confidence_badge():
    assert confidence_badge(90) == "High"
    assert confidence_badge(70) == "Medium"
    assert confidence_badge(40) == "Needs Review"


def test_workflow_mermaid_contains_agents():
    diagram = workflow_mermaid()
    assert "Planning Agent" in diagram
    assert "Evidence Validator" in diagram
