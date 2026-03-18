// Parameter file for the 'prod' environment
// Reference: https://learn.microsoft.com/azure/azure-resource-manager/bicep/parameter-files

using '../main.bicep'

param environmentName = 'prod'
param appName = 'haleon-assistant'
// TODO: add environment-specific parameter overrides below
