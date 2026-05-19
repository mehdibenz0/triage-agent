#!/usr/bin/env bash
set -euo pipefail

API_URL="${1:-http://localhost:8000/classify}"

curl -sS -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  --data @examples/sample_payload_hr.json | python -m json.tool
