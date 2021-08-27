locals {
  frontend_endpoints = local.is_prod ? ["fe-askoptum", "fe-askoptum-www"] : ["fe-askoptum"]
}
resource "azurerm_frontdoor" "edge" {
  name                                         = "${local.namespace-}fd-askoptum-${var.runiac_environment}"
  resource_group_name                          = azurerm_resource_group.app.name
  enforce_backend_pools_certificate_name_check = false

  routing_rule {
    name               = "rr-app-http"
    accepted_protocols = ["Http"]
    patterns_to_match  = ["/*"]
    frontend_endpoints = local.frontend_endpoints
    redirect_configuration {
      redirect_protocol = "HttpsOnly"
      redirect_type     = "Moved"
    }
  }

  routing_rule {
    name               = "rr-app-https"
    accepted_protocols = ["Https"]
    patterns_to_match  = ["/*"]
    frontend_endpoints = local.frontend_endpoints
    forwarding_configuration {
      backend_pool_name             = "be-frontend"
      cache_enabled                 = !local.is_ephemeral
      cache_use_dynamic_compression = true
    }
  }

  routing_rule {
    name               = "rr-backend-https"
    accepted_protocols = ["Https"]
    patterns_to_match  = ["/api/*", "/auth/*"]
    frontend_endpoints = local.frontend_endpoints
    forwarding_configuration {
      backend_pool_name = "be-backend"
    }
  }

  backend_pool_load_balancing {
    name = "default"
  }

  backend_pool_health_probe {
    name = "default"
  }

  backend_pool_health_probe {
    name                = "indexhtml"
    enabled             = true
    interval_in_seconds = 120
    path                = "/index.html"
  }

  backend_pool {
    name = "be-backend"
    backend {
      host_header = azurerm_app_service.backend.default_site_hostname
      address     = azurerm_app_service.backend.default_site_hostname
      http_port   = 80
      https_port  = 443
    }

    load_balancing_name = "default"
    health_probe_name   = "default"
  }

  backend_pool {
    name = "be-frontend"
    backend {
      host_header = azurerm_storage_account.web.primary_web_host
      address     = azurerm_storage_account.web.primary_web_host
      http_port   = 80
      https_port  = 443
    }

    load_balancing_name = "default"
    health_probe_name   = "indexhtml"
  }

  frontend_endpoint {
    name      = "default"
    host_name = "${local.namespace-}fd-askoptum-${var.runiac_environment}.azurefd.net"
  }

  frontend_endpoint {
    name      = "fe-askoptum"
    host_name = trimsuffix(azurerm_dns_cname_record.cname.fqdn, ".")
  }

  dynamic "frontend_endpoint" {
    for_each = local.is_prod ? [1] : []
    content {
      name      = "fe-askoptum-www"
      host_name = trimsuffix(azurerm_dns_cname_record.www.0.fqdn, ".")
    }
  }
}

data "azurerm_resource_group" "askoptum" {
  name = "askoptum"
}

data "azurerm_dns_zone" "askoptum" {
  name                = "ask.optum.ai"
  resource_group_name = data.azurerm_resource_group.askoptum.name
}

resource "azurerm_dns_cname_record" "cname" {
  name                = local.is_ephemeral ? var.runiac_namespace : var.runiac_environment
  zone_name           = data.azurerm_dns_zone.askoptum.name
  resource_group_name = data.azurerm_resource_group.askoptum.name
  ttl                 = local.is_ephemeral ? 10 : 300
  record              = "${local.namespace-}fd-askoptum-${var.runiac_environment}.azurefd.net"
}

resource "azurerm_frontdoor_custom_https_configuration" "askoptum" {
  for_each                          = azurerm_frontdoor.edge.frontend_endpoints
  frontend_endpoint_id              = each.value
  custom_https_provisioning_enabled = true
  custom_https_configuration {}
}

# TODO: Need to BYO certificate before we can use this on front door
# resource azurerm_dns_a_record apex {
#   count               = local.is_prod ? 1 : 0
#   name                = "@"
#   zone_name           = data.azurerm_dns_zone.askoptum.name
#   resource_group_name = data.azurerm_resource_group.askoptum.name
#   ttl                 = 300
#   target_resource_id  = azurerm_frontdoor.edge.id
# }

# resource azurerm_dns_cname_record afdverify {
#   count               = local.is_prod ? 1 : 0
#   name                = "afdverify"
#   zone_name           = data.azurerm_dns_zone.askoptum.name
#   resource_group_name = data.azurerm_resource_group.askoptum.name
#   ttl                 = 60
#   record              = "afdverify.fd-askoptum-${var.runiac_environment}.azurefd.net"
# }

resource "azurerm_dns_cname_record" "www" {
  count               = local.is_prod ? 1 : 0
  name                = "www"
  zone_name           = data.azurerm_dns_zone.askoptum.name
  resource_group_name = data.azurerm_resource_group.askoptum.name
  ttl                 = 300
  record              = "fd-askoptum-${var.runiac_environment}.azurefd.net"
}