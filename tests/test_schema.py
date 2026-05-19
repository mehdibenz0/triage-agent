from triage_agent.claude_classifier import triage_json_schema


def test_schema_contains_required_contract_fields():
    schema = triage_json_schema()
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert "intent" in schema["required"]
    assert "recommended_action" in schema["required"]
    assert "needs_human_review" in schema["required"]
