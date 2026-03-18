// Parameter file for the 'staging' environment
// Reference: https://learn.microsoft.com/azure/azure-resource-manager/bicep/parameter-files

using '../main.bicep'

param environmentName = 'staging'
param appName = 'haleon-assistant'
// TODO: add environment-specific parameter overrides below
