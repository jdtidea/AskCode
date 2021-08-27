resource "azurerm_application_insights" "app" {
  name                = "${local.namespace-}app-askoptum-${var.runiac_environment}-${var.runiac_region}"
  location            = var.runiac_region
  resource_group_name = azurerm_resource_group.app.name
  application_type    = "web"
}

resource "azurerm_log_analytics_workspace" "askoptum" {
  name                = "${local.namespace-}logs-askoptum-${var.runiac_environment}"
  location            = var.runiac_region
  resource_group_name = azurerm_resource_group.app.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}