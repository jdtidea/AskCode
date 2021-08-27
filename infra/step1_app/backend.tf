terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "statctfstate${var.runiac_environment}"
    container_name       = "tfstate"
    key                  = "askoptum-${var.runiac_step}.terraform.tfstate"
  }
}
