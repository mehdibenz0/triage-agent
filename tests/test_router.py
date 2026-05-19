from triage_agent.router import choose_route
from triage_agent.schemas import TriageDecision


def decision(**overrides):
    base = {
        "intent": "hr_benefits",
        "urgency": "medium",
        "confidence": 0.9,
        "summary": "A normal operations request.",
        "extracted_entities": {},
        "recommended_owner": "operations",
        "recommended_action": "Review and answer the request.",
        "sla_hours": 24,
        "needs_human_review": False,
        "reasoning_brief": "The request is clear and non-urgent.",
    }
    base.update(overrides)
    return TriageDecision.model_validate(base)


def test_high_priority_goes_to_urgent_slack():
    route, _ = choose_route(decision(urgency="high"))
    assert route == "slack_urgent"


def test_ambiguous_low_confidence_goes_to_email_fallback():
    route, _ = choose_route(decision(needs_human_review=True))
    assert route == "email_fallback"


def test_spam_is_ignored():
    route, _ = choose_route(decision(intent="spam_or_irrelevant", recommended_owner="ignore"))
    assert route == "ignore"
