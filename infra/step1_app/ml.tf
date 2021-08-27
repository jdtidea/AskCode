resource "azurerm_machine_learning_workspace" "askoptum" {
  name                    = "${local.namespace-}aoml-${var.runiac_environment}-${var.runiac_region}"
  location                = var.runiac_region
  resource_group_name     = azurerm_resource_group.app.name
  application_insights_id = azurerm_application_insights.app.id
  key_vault_id            = data.azurerm_key_vault.askoptum.id
  storage_account_id      = azurerm_storage_account.ml.id
  container_registry_id   = data.azurerm_container_registry.askoptum.id

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_storage_account" "ml" {
  name                     = "st${var.runiac_namespace}aoml${var.runiac_environment}${module.azure-region.location_short}"
  resource_group_name      = azurerm_resource_group.app.name
  location                 = var.runiac_region
  account_tier             = "Standard"
  account_replication_type = "GRS"
}