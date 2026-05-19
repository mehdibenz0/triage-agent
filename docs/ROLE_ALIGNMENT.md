# Why this project fits the Junior AI & Automation Project Manager role

This project directly demonstrates the core capabilities described in the job posting:

| Job need | What the repo shows |
|---|---|
| Design and deploy AI agents | A working classifier service plus workflow orchestration |
| n8n or equivalent | Importable n8n workflow JSON |
| Connect internal tools | Webhook intake and Slack/email routing pattern |
| Measure impact | Metrics and registry documentation |
| Maintain live agent registry | `docs/AGENT_REGISTRY.md` |
| Cross-functional thinking | Owners, escalation paths, human review |
| Method and rigour | Tests, architecture docs, `.env`, Docker, examples |
| AI fundamentals | Structured outputs, stable schema, confidence handling |

## How to describe it in an interview

> “I built a triage automation for inbound business requests. n8n handles the orchestration and Claude returns a schema-constrained classification that includes intent, urgency, owner, action, and SLA. The workflow then routes urgent issues to a dedicated Slack channel, normal cases to a triage queue, and ambiguous items to human review. I documented the agent registry, operational metrics, architecture, setup, and risk mitigations because I wanted the project to look like something a transformation team could actually deploy, not just a toy LLM demo.”
