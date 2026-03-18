# Runbook

## Health Check

```bash
curl https://<your-app-url>/api/v1/health
```

Expected response: `{"status": "ok", "uptime_seconds": <number>}`

## Common Issues

### App fails to start

1. Check environment variables are set (see `.env.example`).
2. Verify Azure credentials: `az account show`.
3. Check application logs: `az webapp log tail --name <app> --resource-group <rg>`.

### Search returns no results

1. Confirm the search index exists: `az search index list ...`.
2. Re-run the ingestion pipeline: `python -m haleon_assistant.ingestion.pipeline`.

### High latency

1. Check Redis cache hit-rate metrics in Application Insights.
2. Review Azure OpenAI token-per-minute quota.

## Escalation

For production incidents, page the on-call engineer via PagerDuty.
For adverse event queries not handled by the assistant, escalate to the
Pharmacovigilance team immediately.

## TODO

- Add detailed Azure Monitor alert runbook entries.
- Document rollback procedure for failed deployments.
