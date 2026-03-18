#!/usr/bin/env bash
# Deploy Haleon AI Assistant infrastructure using Azure Bicep.
# Usage: ./deploy.sh <RESOURCE_GROUP> <LOCATION> <PREFIX>
set -euo pipefail

RESOURCE_GROUP="${1:?Usage: $0 <RESOURCE_GROUP> <LOCATION> <PREFIX>}"
LOCATION="${2:?Usage: $0 <RESOURCE_GROUP> <LOCATION> <PREFIX>}"
PREFIX="${3:?Usage: $0 <RESOURCE_GROUP> <LOCATION> <PREFIX>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Creating resource group: $RESOURCE_GROUP in $LOCATION"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

echo "==> Deploying Bicep template..."
DEPLOYMENT_OUTPUT=$(az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file "$SCRIPT_DIR/main.bicep" \
  --parameters resourcePrefix="$PREFIX" location="$LOCATION" \
  --output json)

KEYVAULT_URI=$(echo "$DEPLOYMENT_OUTPUT" | jq -r '.properties.outputs.keyVaultUri.value')
# Extract vault name from URI (e.g. https://haleon-kv.vault.azure.net/ → haleon-kv)
KEYVAULT_NAME=$(echo "$KEYVAULT_URI" | sed 's|https://||' | cut -d'.' -f1)
echo "==> Key Vault: $KEYVAULT_NAME (URI: $KEYVAULT_URI)"

# Store secrets in Key Vault from environment variables (if set)
store_secret() {
  local secret_name="$1"
  local env_var="$2"
  local value="${!env_var:-}"
  if [[ -n "$value" ]]; then
    echo "==> Storing secret: $secret_name"
    az keyvault secret set \
      --vault-name "$KEYVAULT_NAME" \
      --name "$secret_name" \
      --value "$value" \
      --output none
  fi
}

store_secret "azure-openai-api-key"          "AZURE_OPENAI_API_KEY"
store_secret "azure-search-key"              "AZURE_SEARCH_KEY"
store_secret "azure-content-safety-key"      "AZURE_CONTENT_SAFETY_KEY"
store_secret "azure-storage-connection-str"  "AZURE_STORAGE_CONNECTION_STRING"

echo "==> Deployment complete."
echo "$DEPLOYMENT_OUTPUT" | jq '.properties.outputs'
