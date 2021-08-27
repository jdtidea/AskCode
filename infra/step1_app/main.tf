resource "azurerm_resource_group" "app" {
  name     = "${local.namespace-}rg-askoptum-app-${var.runiac_environment}-${var.runiac_region}"
  location = var.runiac_region
}

module "azure-region" {
  source       = "../modules/regions"
  azure_region = var.runiac_region
}

resource "azurerm_app_service_plan" "backend" {
  name                = "${local.namespace-}plan-askoptum-${var.runiac_environment}-${var.runiac_region}"
  location            = var.runiac_region
  resource_group_name = azurerm_resource_group.app.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Standard"
    size = "S1"
  }
}


resource "azurerm_app_service" "backend" {
  name                = "${local.namespace-}app-askoptum-${var.runiac_environment}-${var.runiac_region}"
  location            = var.runiac_region
  resource_group_name = azurerm_resource_group.app.name
  app_service_plan_id = azurerm_app_service_plan.backend.id
  https_only          = true

  site_config {
    ftps_state        = "Disabled"
    linux_fx_version  = "DOCKER|${data.azurerm_container_registry.askoptum.login_server}/${var.docker_image}:${var.docker_tag}"
    http2_enabled     = true
    always_on         = true
    health_check_path = "/api/health"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_PASSWORD"       = data.azurerm_container_registry.askoptum.admin_password
    "DOCKER_REGISTRY_SERVER_URL"            = "https://${data.azurerm_container_registry.askoptum.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME"       = data.azurerm_container_registry.askoptum.admin_username
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE"   = false
    "DOCKER_ENABLE_CI"                      = local.is_ephemeral ? true : null
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.app.connection_string
    "APP_CONFIG_CONNECTION_STRING"          = data.azurerm_app_configuration.config.secondary_read_key.0.connection_string
  }
}

resource "null_resource" "configure_container_cicd" {
  // configure automated deployments when ephemeral deployments (mutable container tags)
  count = local.is_ephemeral ? 1 : 1
  triggers = {
    app_service             = azurerm_app_service.backend.name
    resource_group          = azurerm_app_service.backend.resource_group_name
    image                   = var.docker_image
    tag                     = var.docker_tag
    registry_name           = data.azurerm_container_registry.askoptum.name
    registry_resource_group = data.azurerm_container_registry.askoptum.resource_group_name
    webhook_name            = replace(azurerm_app_service.backend.name, "-", "")
  }

  provisioner "local-exec" {
    command = <<EOT
    az acr webhook create --name ${self.triggers.webhook_name} --registry ${self.triggers.registry_name} --resource-group ${self.triggers.registry_resource_group} --actions push --uri `az webapp deployment container config --name ${self.triggers.app_service} --resource-group ${self.triggers.resource_group} --enable-cd true --query CI_CD_URL --output tsv` --scope '${self.triggers.image}:${self.triggers.tag}'
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<EOT
      az acr webhook delete --name ${self.triggers.webhook_name} --registry ${self.triggers.registry_name}
      EOT
  }
}

data "azurerm_container_registry" "askoptum" {
  name                = "askoptum1"
  resource_group_name = "askoptum"
}

data "azurerm_app_configuration" "config" {
  name                = "conf-askoptum-${var.runiac_environment}"
  resource_group_name = "rg-askoptum-${var.runiac_environment}"
}