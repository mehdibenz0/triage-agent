import json
from pathlib import Path

from triage_agent.normalizers import normalize_payload


def test_generic_payload_normalizes():
    payload = json.loads(Path("examples/sample_payload_hr.json").read_text())["payload"]
    request = normalize_payload(payload)
    assert request.submission_id == "demo-hr-001"
    assert request.requester_email == "sophie.martin@example.ch"
    assert request.source.value == "web_form"


def test_typeform_like_payload_normalizes():
    payload = json.loads(Path("examples/typeform_like_payload.json").read_text())
    request = normalize_payload(payload)
    assert request.submission_id == "tf-demo-003"
    assert request.requester_email == "nora.keller@example.ch"
    assert request.source.value == "typeform"
