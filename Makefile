.PHONY: install run test docker-up docker-down demo lint-json

install:
	python -m pip install -r requirements.txt

run:
	PYTHONPATH=src uvicorn triage_agent.api:app --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=src pytest -q

docker-up:
	docker compose up --build

docker-down:
	docker compose down

demo:
	bash scripts/send_test_webhook.sh

lint-json:
	python -m json.tool workflow.json > /dev/null
	python -m json.tool examples/sample_payload_hr.json > /dev/null
	python -m json.tool examples/sample_payload_urgent_ops.json > /dev/null
