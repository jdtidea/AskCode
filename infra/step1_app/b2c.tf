resource "null_resource" "update_redirect_uri" {
  triggers = {
    app_id        = var.runiac_environment == "prod" ? "a8f89630-fd6c-4176-9134-d3d05ef7dc00" : "019d0151-d35b-4716-a2a8-c275b8709308"
    new_uri       = "https://${trimsuffix(azurerm_dns_cname_record.cname.fqdn, ".")}/auth"
    b2c_tenant_id = var.runiac_environment == "prod" ? "d8b3e1e3-9078-417f-9c3b-d24536be9e09" : "42e9a1eb-ce76-4702-a369-7fdde8de9554"
    b2c_client_id = var.runiac_environment == "prod" ? "11e3d3c7-5d5f-4b01-b203-88271654972e" : "09121524-9906-4fb8-bfd9-c45c41ad8450"
    is_prod       = var.runiac_environment == "prod" ? "true" : "false"
  }
  provisioner "local-exec" {
    command = <<EOT
 (export AZURE_CONFIG_DIR="~/azuretemp";
 az login --service-principal --username ${self.triggers.b2c_client_id} --password="$B2C_CLIENT_SECRET" --tenant ${self.triggers.b2c_tenant_id} --allow-no-subscriptions || exit 1;
 SPA_OLD_URIS=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/applications/${self.triggers.app_id}" | jq -c '.spa.redirectUris | unique')
 SPA_NEW_URIS=$(printf '%s\n' "$SPA_OLD_URIS" | jq -c ". + [\"${self.triggers.new_uri}\"] | unique")

 if [ "x$SPA_NEW_URIS" != "x$SPA_OLD_URIS" ]; then
  SPA_PATCH=$(printf '%s\n' "$SPA_NEW_URIS" | jq -c '{"spa":{"redirectUris":.}}')
  az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/${self.triggers.app_id}" --headers 'Content-Type=application/json' --body="$SPA_PATCH" || exit 1
 fi)
 EOT
  }
  provisioner "local-exec" {
    when    = destroy
    command = <<EOT
 if [ "${self.triggers.is_prod}" == "true" ]; then
  echo "Skipping destroy for prod..."
  exit 0;
 fi
 (export AZURE_CONFIG_DIR="~/azuretemp";
 az login --service-principal --username ${self.triggers.b2c_client_id} --password="$B2C_CLIENT_SECRET" --tenant ${self.triggers.b2c_tenant_id} --allow-no-subscriptions;
 SPA_OLD_URIS=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/applications/${self.triggers.app_id}" | jq -c '.spa.redirectUris | unique')
 SPA_NEW_URIS=$(printf '%s\n' "$SPA_OLD_URIS" | jq 'del(.[] | select(. == "${self.triggers.new_uri}"))')
 if [ "x$SPA_NEW_URIS" != "x$SPA_OLD_URIS" ]; then
  SPA_PATCH=$(printf '%s\n' "$SPA_NEW_URIS" | jq -c '{"spa":{"redirectUris":.}}')
  az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/applications/${self.triggers.app_id}" --headers 'Content-Type=application/json' --body="$SPA_PATCH" || exit 1
 fi)
 EOT
  }
}