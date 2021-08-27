#!/bin/sh

if [[ -z "$ARM_CLIENT_ID" || -z "$ARM_CLIENT_SECRET" || -z "$ARM_TENANT_ID"  || -z "$ARM_SUBSCRIPTION_ID" ]]; then
  if az account get-access-token ; then
    echo "already logged in..."
  else
    az login || exit 1;
  fi
else
  az login --service-principal --username "$ARM_CLIENT_ID" --password "$ARM_CLIENT_SECRET" --tenant "$ARM_TENANT_ID"
fi

az account set -s "${RUNIAC_ACCOUNT_ID}"

# TODO: Store client secret in prod key vault, and change command accordingly
if [[ $RUNIAC_ENVIRONMENT == "prod" ]]
then
    export B2C_CLIENT_SECRET=$(az keyvault secret show  --name askoptum-b2c-automation-secret-prod \
    --subscription 10abbbc1-99ca-4088-bcab-01bd44ae1cf9 \
    --vault-name atccommonkeyvault --query 'value' -o tsv)
else
    export B2C_CLIENT_SECRET=$(az keyvault secret show  --name lab-b2c-automation-secret \
    --subscription 10abbbc1-99ca-4088-bcab-01bd44ae1cf9 \
    --vault-name atccommonkeyvault --query 'value' -o tsv)
fi

runiac