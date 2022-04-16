resource "azurerm_firewall_policy_rule_collection_group" "common" {
  name               = "common"
  firewall_policy_id = azurerm_firewall_policy.demo.id
  priority           = 100

  application_rule_collection {
    name     = "commonFqdns"
    priority = 200
    action   = "Allow"

    rule {
      name = "AzureTags"
      protocols {
        type = "Https"
        port = 443
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdn_tags = [
        "AzureKubernetesService",
      ]
    }

    rule {
      name = "Ubuntu"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "ubuntu.com",
        "*.ubuntu.com",
      ]
    }

    rule {
      name = "Github"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "github.com",
        "*.github.com",
        "*.github.io",
        "*.githubusercontent.com"
      ]
    }

    rule {
      name = "GitOps"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "*.dp.kubernetesconfiguration.azure.com",
      ]
    }

    rule {
      name = "ARM"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "management.azure.com",
      ]
    }

    rule {
      name = "aka.ms"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "aka.ms",
      ]
    }

    rule {
      name = "repos"
      protocols {
        type = "Https"
        port = 443
      }
      protocols {
        type = "Http"
        port = 80
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "azurecliprod.blob.core.windows.net",
        "packages.microsoft.com",
        "dl.k8s.io",
        "storage.googleapis.com",
        "charts.jetstack.io",
        "quay.io",
        "*.quay.io",
        "k8s.gcr.io",
        "ghcr.io",
        "mcr.microsoft.com"
      ]
    }
  }

  application_rule_collection {
    name     = "APIM"
    priority = 210
    action   = "Allow"

    rule {
      name = "APIM"
      protocols {
        type = "Https"
        port = 443
      }
      source_addresses = ["10.0.0.0/8"]

      destination_fqdns = [
        "${azurerm_api_management.demo.name}.configuration.azure-api.net",
      ]
    }
  }

  network_rule_collection {
    name     = "commonNetworks"
    priority = 100
    action   = "Allow"

    rule {
      name                  = "aks"
      source_addresses      = ["10.0.0.0/8"]
      destination_addresses = ["AzureCloud"]
      destination_ports     = ["1194", "9000"]
      protocols             = ["Any"]
    }

    rule {
      name                  = "ntp"
      source_addresses      = ["10.0.0.0/8"]
      destination_addresses = ["AzureCloud"]
      destination_ports     = ["123"]
      protocols             = ["UDP"]
    }
  }

  network_rule_collection {
    name     = "apimDemo"
    priority = 120
    action   = "Allow"

    rule {
      name                  = "aks"
      source_addresses      = ["10.0.0.0/8"]
      destination_addresses = [azurerm_api_management.demo.public_ip_addresses.0]
      destination_ports     = ["443"]
      protocols             = ["Any"]
    }
  }
}
