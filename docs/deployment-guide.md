# Deployment Guide

## Prerequisites

- Azure CLI ≥ 2.50
- Bicep CLI ≥ 0.20 (included with Azure CLI)
- Contributor access to the target Azure subscription

## Environments

| Environment | Parameter file |
|-------------|---------------|
| Development | `infra/parameters/dev.bicepparam` |
| Staging | `infra/parameters/staging.bicepparam` |
| Production | `infra/parameters/prod.bicepparam` |

## Deploy to Development

```bash
# 1. Log in
az login

# 2. Create resource group (first time)
az group create --name rg-haleon-assistant-dev --location uksouth

# 3. Deploy
az deployment group create \
  --resource-group rg-haleon-assistant-dev \
  --template-file infra/main.bicep \
  --parameters infra/parameters/dev.bicepparam
```

## Docker

```bash
docker build -t haleon-assistant .
docker run -p 8000:8000 --env-file .env haleon-assistant
```

## docker-compose

```bash
docker-compose up --build
```

## Next Steps

- Configure GitHub Actions OIDC for passwordless Azure deployments.
- Add Key Vault references for secrets in the parameter files.
- Enable Azure Monitor and Application Insights (see `infra/modules/app-insights.bicep`).
