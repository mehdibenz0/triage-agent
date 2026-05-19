from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .claude_classifier import classify_request
from .normalizers import normalize_payload
from .router import build_classification_response, slack_message


app = FastAPI(
    title="AI Triage Agent",
    version="1.0.0",
    description="Webhook-compatible triage service for n8n + Claude structured classification.",
)


class RawPayload(BaseModel):
    payload: dict


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify")
def classify(raw: RawPayload) -> dict:
    try:
        request = normalize_payload(raw.payload)
        decision = classify_request(request)
        response = build_classification_response(request, decision)
        return response.model_dump(mode="json")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/format-slack")
def format_slack(raw: dict) -> dict[str, str]:
    try:
        from .schemas import ClassificationResponse

        response = ClassificationResponse.model_validate(raw)
        return slack_message(response)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
