from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class Intent(str, Enum):
    HR_BENEFITS = "hr_benefits"
    CUSTOMER_SUPPORT = "customer_support"
    PARTNERSHIPS = "partnerships"
    TECHNICAL_ISSUE = "technical_issue"
    FINANCE_BILLING = "finance_billing"
    GENERAL_REQUEST = "general_request"
    SPAM_OR_IRRELEVANT = "spam_or_irrelevant"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InputChannel(str, Enum):
    TYPEFORM = "typeform"
    WEB_FORM = "web_form"
    CRM = "crm"
    ESM = "esm"
    EMAIL = "email"
    API = "api"
    UNKNOWN = "unknown"


class TriageRequest(BaseModel):
    submission_id: str = Field(..., min_length=1, description="Unique submission/request ID.")
    submitted_at: datetime | None = Field(default=None)
    source: InputChannel = Field(default=InputChannel.UNKNOWN)
    requester_name: str | None = None
    requester_email: str | None = None
    company: str | None = None
    subject: str = Field(..., min_length=2, max_length=300)
    message: str = Field(..., min_length=5, max_length=12000)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("requester_email", mode="before")
    @classmethod
    def normalize_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return str(value).strip().lower()


class TriageDecision(BaseModel):
    intent: Intent
    urgency: Urgency
    confidence: float = Field(..., ge=0.0, le=1.0)
    summary: str = Field(..., min_length=5, max_length=320)
    extracted_entities: dict[str, list[str]] = Field(default_factory=dict)
    recommended_owner: Literal[
        "operations",
        "customer_service",
        "partnerships",
        "finance",
        "tech",
        "ignore",
    ]
    recommended_action: str = Field(..., min_length=5, max_length=320)
    sla_hours: int = Field(..., ge=0, le=168)
    needs_human_review: bool
    reasoning_brief: str = Field(..., min_length=5, max_length=240)


class ClassificationResponse(BaseModel):
    request: TriageRequest
    triage: TriageDecision
    route: Literal["slack_urgent", "slack_triage", "email_fallback", "ignore"]
    routing_reason: str


class SlackMessage(BaseModel):
    text: str
