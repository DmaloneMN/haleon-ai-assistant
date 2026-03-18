// Haleon AI Assistant – Bicep orchestrator
// TODO: update module paths and parameter references before deploying.

targetScope = 'resourceGroup'

// ---------------------------------------------------------------------------
// Parameters (values come from the environment parameter file)
// ---------------------------------------------------------------------------
param location string = resourceGroup().location
param environmentName string
param appName string = 'haleon-assistant'

// ---------------------------------------------------------------------------
// Module references
// ---------------------------------------------------------------------------
module openai 'modules/openai.bicep' = {
  name: 'openai'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module search 'modules/search.bicep' = {
  name: 'search'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module keyvault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module redis 'modules/redis.bicep' = {
  name: 'redis'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module apim 'modules/apim.bicep' = {
  name: 'apim'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module contentSafety 'modules/content-safety.bicep' = {
  name: 'content-safety'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module eventhub 'modules/eventhub.bicep' = {
  name: 'eventhub'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module appInsights 'modules/app-insights.bicep' = {
  name: 'app-insights'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}

module networking 'modules/networking.bicep' = {
  name: 'networking'
  params: {
    location: location
    environmentName: environmentName
    appName: appName
  }
}
