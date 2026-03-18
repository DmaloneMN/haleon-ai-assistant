@description('Azure region')
param location string

@description('Resource name for the Cognitive Services account')
param name string

@description('Name of the GPT model deployment')
param deploymentName string

@description('Cognitive Services SKU')
param skuName string = 'S0'

resource openAiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  kind: 'OpenAI'
  sku: {
    name: skuName
  }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
  }
}

resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiAccount
  name: deploymentName
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-05-13'
    }
  }
}

output endpoint string = openAiAccount.properties.endpoint
output name string = openAiAccount.name
