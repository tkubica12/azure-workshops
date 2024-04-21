resource "azurerm_orchestrated_virtual_machine_scale_set" "main" {
  name                        = module.naming.linux_virtual_machine_scale_set.name
  resource_group_name         = var.resource_group_name
  location                    = var.location
  platform_fault_domain_count = 1
  sku_name                    = var.vm_size
  zones                       = ["1", "2", "3"]
  zone_balance                = true
  instances                   = 2
  source_image_id             = var.image_id

  os_profile {
    linux_configuration {
      disable_password_authentication = false
      admin_username                  = "tomas"
      admin_password                  = "Azure12345678"
    }
  }

  network_interface {
    name    = module.naming.network_interface.name
    primary = true

    ip_configuration {
      name      = "internal"
      primary   = true
      subnet_id = var.subnet_id
    }
  }

  boot_diagnostics {}

  extension {
    name                               = "HealthExtension"
    publisher                          = "Microsoft.ManagedServices"
    type                               = "ApplicationHealthLinux "
    type_handler_version               = "2.0"
    auto_upgrade_minor_version_enabled = true

    settings = jsonencode({
      "protocol"          = "http"
      "port"              = "80"
      "requestPath"       = "/"
      "intervalInSeconds" = 2
      "numberOfProbes"    = 3
    })
  }
}
