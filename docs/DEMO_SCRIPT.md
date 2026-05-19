# 30-second Loom / GIF Demo Script

Record this exact flow:

**0–5 seconds**  
Show the repository homepage and say:  
“Here is an AI triage automation I built for operations teams.”

**5–12 seconds**  
Open n8n and briefly show the workflow:  
Webhook → classifier API → route switch → Slack/email.

**12–20 seconds**  
Send the sample urgent payload:
```bash
bash scripts/send_test_webhook.sh
```

**20–27 seconds**  
Show the Slack notification appearing with:
- urgency
- intent
- recommended owner
- action
- SLA

**27–30 seconds**  
End on the README architecture diagram and say:  
“The point is not only classification; it is a deployable business workflow with human review and measurable impact.”

## Suggested repo asset name
- `assets/demo.gif`
or
- `assets/demo-loom-link.md`
