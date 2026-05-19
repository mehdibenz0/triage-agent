from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .schemas import InputChannel, TriageRequest


def normalize_generic_payload(payload: dict[str, Any]) -> TriageRequest:
    """Normalize a mock form/CRM/ESM payload into the internal request contract."""
    return TriageRequest(
        submission_id=str(payload.get("submission_id") or payload.get("id") or uuid4()),
        submitted_at=payload.get("submitted_at") or datetime.now(timezone.utc).isoformat(),
        source=payload.get("source", InputChannel.API.value),
        requester_name=payload.get("requester_name") or payload.get("name"),
        requester_email=payload.get("requester_email") or payload.get("email"),
        company=payload.get("company"),
        subject=payload.get("subject") or "Untitled request",
        message=payload.get("message") or payload.get("description") or "",
        metadata=payload.get("metadata", {}),
    )


def normalize_typeform_like_payload(payload: dict[str, Any]) -> TriageRequest:
    """Handle a simplified Typeform-like nested payload for portfolio/demo purposes."""
    form_response = payload.get("form_response", {})
    hidden = form_response.get("hidden", {})
    answers = form_response.get("answers", [])

    answer_map: dict[str, str] = {}
    for answer in answers:
        field = answer.get("field", {})
        key = field.get("ref") or field.get("id")
        if not key:
            continue
        answer_value = (
            answer.get("text")
            or answer.get("email")
            or answer.get("choice", {}).get("label")
            or str(answer.get("number", ""))
        )
        answer_map[key] = answer_value

    return TriageRequest(
        submission_id=str(form_response.get("token") or uuid4()),
        submitted_at=form_response.get("submitted_at"),
        source=InputChannel.TYPEFORM,
        requester_name=answer_map.get("name"),
        requester_email=answer_map.get("email"),
        company=answer_map.get("company"),
        subject=answer_map.get("subject") or "Typeform request",
        message=answer_map.get("message") or "",
        metadata={"hidden": hidden, "source_event": payload.get("event_type", "form_response")},
    )


def normalize_payload(payload: dict[str, Any]) -> TriageRequest:
    if "form_response" in payload:
        return normalize_typeform_like_payload(payload)
    return normalize_generic_payload(payload)
