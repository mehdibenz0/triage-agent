# Live Agent Registry

This document mirrors the kind of live registry an Operations/PMO team would maintain for deployed AI automations.

| Field | Value |
|---|---|
| Agent name | AI Triage Agent |
| Owner | Operations / PMO |
| Business sponsor | Chief Transformation Officer / AI Ambassadors |
| Primary user | Internal operations triage team |
| Trigger | Incoming form, CRM, ESM, or API request |
| LLM | Claude, configured by environment variable |
| Workflow orchestrator | n8n |
| Outputs | Structured triage decision, routing destination, Slack/email notification |
| Human-in-the-loop | Yes, via `needs_human_review` and fallback routing |
| Monitoring | Classification logs, route distribution, false-positive review, SLA adherence |
| Data sensitivity | Request text may contain business/customer information; redact in logs where needed |
| Failure mode | API failure, low-confidence classification, downstream webhook error |
| Rollback | Disable n8n workflow and revert to manual inbox triage |

## Metrics to track

1. Median time from submission to first routing action.
2. Share of requests auto-routed without human override.
3. False routing rate from reviewed samples.
4. Percentage of high/critical items acknowledged within SLA.
5. Volume by intent and source system.

## Iteration backlog

- Add Jira/Confluence enrichment for known projects.
- Push accepted requests to CRM/ESM.
- Add a small evaluation dataset and score intent accuracy.
- Add PII redaction before LLM submission for production hardening.
