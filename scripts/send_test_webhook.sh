#!/usr/bin/env bash
set -euo pipefail

WEBHOOK_URL="${1:-http://localhost:5678/webhook/ai-triage-agent}"

curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  --data @examples/sample_payload_urgent_ops.json | python -m json.tool
