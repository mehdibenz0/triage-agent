from __future__ import annotations

import json
from typing import Any

import httpx

from .config import settings
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .schemas import TriageDecision, TriageRequest


def triage_json_schema() -> dict[str, Any]:
    # A compact, explicit JSON Schema keeps the API contract human-auditable.
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "intent": {
                "type": "string",
                "enum": [
                    "hr_benefits",
                    "customer_support",
                    "partnerships",
                    "technical_issue",
                    "finance_billing",
                    "general_request",
                    "spam_or_irrelevant",
                ],
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"],
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
            "summary": {"type": "string"},
            "extracted_entities": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "recommended_owner": {
                "type": "string",
                "enum": [
                    "operations",
                    "customer_service",
                    "partnerships",
                    "finance",
                    "tech",
                    "ignore",
                ],
            },
            "recommended_action": {"type": "string"},
            "sla_hours": {
                "type": "integer",
                "minimum": 0,
                "maximum": 168,
            },
            "needs_human_review": {"type": "boolean"},
            "reasoning_brief": {"type": "string"},
        },
        "required": [
            "intent",
            "urgency",
            "confidence",
            "summary",
            "extracted_entities",
            "recommended_owner",
            "recommended_action",
            "sla_hours",
            "needs_human_review",
            "reasoning_brief",
        ],
    }


def _extract_text(response_json: dict[str, Any]) -> str:
    content_blocks = response_json.get("content", [])
    texts = [
        block.get("text", "")
        for block in content_blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    if not texts:
        raise ValueError("Claude response did not contain a text block.")
    return "".join(texts).strip()


def classify_request(request: TriageRequest) -> TriageDecision:
    if not settings.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is missing. Copy .env.example to .env and set a real key."
        )

    payload = request.model_dump(mode="json")
    body = {
        "model": settings.anthropic_model,
        "max_tokens": 900,
        "temperature": 0,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": build_user_prompt(json.dumps(payload, ensure_ascii=False)),
            }
        ],
        "output_config": {
            "format": {
                "type": "json_schema",
                "schema": triage_json_schema(),
            }
        },
    }

    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": settings.anthropic_version,
        "content-type": "application/json",
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(
                settings.anthropic_api_url,
                headers=headers,
                json=body,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:1200]
        raise RuntimeError(f"Anthropic API returned {exc.response.status_code}: {detail}") from exc
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Anthropic API request failed: {exc}") from exc

    raw_text = _extract_text(response.json())
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Claude returned non-JSON text despite structured output: {raw_text}") from exc

    return TriageDecision.model_validate(parsed)
