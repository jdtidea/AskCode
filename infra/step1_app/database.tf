//resource "azurerm_postgresql_server" "example" {
//  name                = "${local.namespace-}psql-askoptum-${var.runiac_environment}-${var.runiac_region}"
//  location            = var.runiac_region
//  resource_group_name = azurerm_resource_group.app.name
//
//  administrator_login          = "psqladminun"
//  administrator_login_password = "H@Sh1CoR3!"
//
//  sku_name   = "GP_Gen5_4"
//  version    = "9.6"
//  storage_mb = 640000
//
//  backup_retention_days        = 7
//  geo_redundant_backup_enabled = true
//  auto_grow_enabled            = true
//
//  public_network_access_enabled    = false
//  ssl_enforcement_enabled          = true
//  ssl_minimal_tls_version_enforced = "TLS1_2"
//}