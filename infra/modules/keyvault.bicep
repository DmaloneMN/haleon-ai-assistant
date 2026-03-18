@description('Azure region')
param location string

@description('Key Vault resource name')
param name string

@description('Azure AD tenant ID')
param tenantId string

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: name
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
  }
}

output uri string = keyVault.properties.vaultUri
output name string = keyVault.name
