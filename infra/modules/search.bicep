@description('Azure region')
param location string

@description('Resource name for the Search service')
param name string

@description('AI Search SKU')
param skuName string = 'standard'

resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: name
  location: location
  sku: {
    name: skuName
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

output endpoint string = 'https://${searchService.name}.search.windows.net'
output name string = searchService.name
