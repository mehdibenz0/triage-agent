from __future__ import annotations

from .schemas import ClassificationResponse, TriageDecision, TriageRequest


def choose_route(decision: TriageDecision) -> tuple[str, str]:
    if decision.intent.value == "spam_or_irrelevant":
        return "ignore", "Request was classified as spam or irrelevant."
    if decision.urgency.value in {"critical", "high"}:
        return "slack_urgent", "High-impact requests are escalated to the urgent operations channel."
    if decision.needs_human_review:
        return "email_fallback", "Low-confidence or ambiguous requests are sent for human review."
    return "slack_triage", "Standard triage requests are routed to the shared operations queue."


def build_classification_response(
    request: TriageRequest,
    decision: TriageDecision,
) -> ClassificationResponse:
    route, reason = choose_route(decision)
    return ClassificationResponse(
        request=request,
        triage=decision,
        route=route,
        routing_reason=reason,
    )


def slack_message(response: ClassificationResponse) -> dict[str, str]:
    triage = response.triage
    req = response.request
    text = (
        f"*AI Triage Agent* — `{triage.urgency.upper()}` / `{triage.intent.value}`\n"
        f"*Subject:* {req.subject}\n"
        f"*Requester:* {req.requester_name or 'Unknown'}"
        f"{f' <{req.requester_email}>' if req.requester_email else ''}\n"
        f"*Summary:* {triage.summary}\n"
        f"*Owner:* {triage.recommended_owner}\n"
        f"*Action:* {triage.recommended_action}\n"
        f"*SLA:* {triage.sla_hours}h\n"
        f"*Human review:* {'yes' if triage.needs_human_review else 'no'}"
    )
    return {"text": text}
