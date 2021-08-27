resource "azurerm_storage_account" "web" {
  name                      = "st${var.runiac_namespace}aoweb${var.runiac_environment}${module.azure-region.location_short}"
  resource_group_name       = azurerm_resource_group.app.name
  location                  = var.runiac_region
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"
  allow_blob_public_access  = false
  static_website {
    error_404_document = "index.html"
    index_document     = "index.html"
  }
  tags = {}
}

resource "azurerm_storage_container" "skill_registry" {
  name                 = "skills"
  storage_account_name = azurerm_storage_account.web.name
}

resource "azurerm_storage_container" "ranking" {
  name                 = "ranking"
  storage_account_name = azurerm_storage_account.web.name
}


data "archive_file" "web_app" {
  type        = "zip"
  source_dir  = var.website_deploy_folder
  output_path = "${path.module}/deploy.zip"
}

resource "null_resource" "copy_files_web" {
  triggers = {
    storage_account_name  = azurerm_storage_account.web.name
    website_deploy_folder = var.website_deploy_folder
    hash                  = data.archive_file.web_app.output_base64sha256
    connection_string     = azurerm_storage_account.web.primary_connection_string
  }

  provisioner "local-exec" {
    command = <<EOT
    az storage blob upload-batch --no-progress --account-name ${self.triggers.storage_account_name} -s ${self.triggers.website_deploy_folder} --connection-string '${self.triggers.connection_string}' -d '$web' --output none

    # set cache control options for static files that should not be cached
    az storage blob update --account-name ${self.triggers.storage_account_name} --container-name '$web' --name index.html --connection-string '${self.triggers.connection_string}' --content-cache-control "max-age=0,no-cache,no-store,must-revalidate"
    EOT
  }
}