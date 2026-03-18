@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Prefix used for all resource names')
param resourcePrefix string

@description('Name of the OpenAI model deployment')
param openAiDeploymentName string = 'gpt-4o'

// --------------------------------------------------
// Modules
// --------------------------------------------------

module openAi 'modules/openai.bicep' = {
  name: 'openai'
  params: {
    location: location
    name: '${resourcePrefix}-openai'
    deploymentName: openAiDeploymentName
  }
}

module search 'modules/search.bicep' = {
  name: 'search'
  params: {
    location: location
    name: '${resourcePrefix}-search'
  }
}

module keyVault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    name: '${resourcePrefix}-kv'
    tenantId: subscription().tenantId
  }
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    name: '${resourcePrefix}-monitor'
  }
}

// --------------------------------------------------
// Storage Account
// --------------------------------------------------

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: replace('${resourcePrefix}stor', '-', '')
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

// --------------------------------------------------
// Outputs
// --------------------------------------------------

output openAiEndpoint string = openAi.outputs.endpoint
output searchEndpoint string = search.outputs.endpoint
output storageEndpoint string = storageAccount.properties.primaryEndpoints.blob
output keyVaultUri string = keyVault.outputs.uri
output appInsightsConnectionString string = monitoring.outputs.appInsightsConnectionString
