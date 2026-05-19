# Project Brief — AI Triage Agent

## Problem
Operations teams receive heterogeneous inbound requests through forms, email, CRM, and service tools. Manual triage slows response times, creates routing errors, and makes it difficult to see where demand is coming from.

## Goal
Create a lightweight AI automation that:
1. Accepts incoming business requests.
2. Classifies intent and urgency.
3. Extracts useful structured fields.
4. Routes the request to the right channel.
5. Preserves human review for ambiguous cases.

## Scope
Included:
- Webhook intake
- Payload normalization
- Claude-powered structured classification
- n8n routing to Slack/email
- Local Docker setup
- Tests and examples
- Architecture and operational documentation

Not included:
- Production authentication gateway
- Persistent database
- Full CRM/ESM write-back
- Enterprise PII redaction layer

## Stakeholders
- Operations / PMO
- AI Ambassadors
- Customer Service
- Partnerships
- Tech / Integrations
- Finance

## Risks and mitigations
| Risk | Mitigation |
|---|---|
| Wrong classification | Structured output, human review branch, review metrics |
| LLM/API downtime | Workflow failure handling and fallback inbox |
| Sensitive content | Avoid logging raw payloads in production; add redaction |
| Scope creep | Keep V1 focused on triage and routing |

## Success criteria
- Requests can be submitted end-to-end through the webhook.
- The classifier returns schema-valid JSON.
- High-priority cases route differently from normal ones.
- The repo can be cloned and run locally with documented steps.
