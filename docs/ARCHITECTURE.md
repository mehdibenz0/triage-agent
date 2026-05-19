# Architecture

```mermaid
flowchart LR
    A[Typeform / CRM / ESM / Mock JSON] --> B[n8n Webhook]
    B --> C[Payload Normalization]
    C --> D[Classifier API: FastAPI]
    D --> E[Claude Structured Output]
    E --> F[Routing Logic]
    F -->|High or Critical| G[Slack Urgent Channel]
    F -->|Normal| H[Slack Triage Channel]
    F -->|Ambiguous| I[Email / Human Review]
    F -->|Spam| J[Ignore + Log]
```

## Design choices

### 1. n8n for orchestration
The workflow is visible to business stakeholders, easy to demo, and directly maps to low-code automation work.

### 2. Python classifier API
The Claude integration is isolated in a small service so the n8n workflow stays readable and reusable. This also makes unit tests possible.

### 3. Strict structured output
The classifier uses a JSON Schema contract so the downstream workflow can route on stable fields such as `urgency`, `intent`, and `recommended_owner`.

### 4. Human review path
Low-confidence or ambiguous cases are explicitly routed for review. This shows operational maturity rather than over-automating.

### 5. Portfolio relevance
This project demonstrates:
- AI agent/automation design
- API integration
- Low-code orchestration
- Business process thinking
- Cross-functional documentation
- Monitoring and deployment discipline
