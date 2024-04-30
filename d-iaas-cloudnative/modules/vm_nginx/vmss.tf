locals {
  configuration     = <<EOF
export keyvaultname=${azurerm_key_vault.main.name}
export storagename=${azurerm_storage_account.main.name}
export identityid=${azurerm_user_assigned_identity.main.id}
EOF
  script_prepare    = file("${path.module}/scripts/prepare.sh")
  script_install    = fileexists("${path.module}/scripts/install_nginx.sh") ? file("${path.module}/scripts/install_nginx.sh") : ""
  script_from_base  = base64encode(join("\n", [local.script_install, local.configuration, local.script_prepare]))
  script_from_image = base64encode(join("\n", [local.configuration, local.script_prepare]))
}

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

  termination_notification {
    enabled = true
    timeout = "PT10M"
  }

  dynamic "source_image_reference" {
    for_each = var.image_id == null ? [1] : []
    content {
      publisher = "canonical"
      offer     = "0001-com-ubuntu-server-jammy"
      sku       = "22_04-lts-gen2"
      version   = "latest"
    }
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }
  automatic_instance_repair {
    enabled      = true
    grace_period = "PT30M"
    # Not supported in AzureRM provider yet is repair type: Restart (just reboot VM, everything preserved), Reimage (OS disk gets replaced, but everything else preserve), Replace (VM gets replaced so private IP, ID, temp and data disk changes)
  }
  os_profile {
    linux_configuration {
      disable_password_authentication = false
      admin_username                  = "tomas"
      admin_password                  = "Azure12345678"
      patch_mode                      = var.image_id != null ? "ImageDefault" : "AutomaticByPlatform"
      patch_assessment_mode           = var.image_id != null ? "ImageDefault" : "ImageDefault"
    }
  }
  os_disk {
    caching              = "ReadOnly"
    storage_account_type = "Standard_LRS"
    diff_disk_settings {
      option    = "Local"
      placement = "ResourceDisk"
    }
  }

  network_interface {
    name    = module.naming.network_interface.name
    primary = true

    ip_configuration {
      name                                   = "internal"
      primary                                = true
      subnet_id                              = var.subnet_id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.main.id]
    }
  }

  boot_diagnostics {}

  extension {
    name                               = "HealthExtension"
    publisher                          = "Microsoft.ManagedServices"
    type                               = "ApplicationHealthLinux"
    type_handler_version               = "2.0"
    auto_upgrade_minor_version_enabled = true

    settings = <<SETTINGS
{
  "protocol": "tcp",
  "port": 80
}
SETTINGS
  }

  extension {
    name                               = "AzureMonitorLinuxAgent"
    publisher                          = "Microsoft.Azure.Monitor"
    type                               = "AzureMonitorLinuxAgent"
    type_handler_version               = "1.0"
    auto_upgrade_minor_version_enabled = true
  }

  extension {
    name                               = "DependencyAgentLinux"
    publisher                          = "Microsoft.Azure.Monitoring.DependencyAgent"
    type                               = "DependencyAgentLinux"
    type_handler_version               = "9.10"
    auto_upgrade_minor_version_enabled = true
    settings                           = <<SETTINGS
{
    "enableAMA": "true"
}
SETTINGS
  }

  extension {
    name                               = "CustomScript"
    publisher                          = "Microsoft.Azure.Extensions"
    type                               = "CustomScript"
    type_handler_version               = "2.1"
    auto_upgrade_minor_version_enabled = true

    protected_settings = <<SETTINGS
{
  "script": "${var.image_id != null ? local.script_from_image : local.script_from_base}"
}
SETTINGS
  }

  depends_on = [
    azurerm_role_assignment.kv_umi,
    azurerm_role_assignment.kv_umi_reader
  ]
}

resource "azurerm_monitor_data_collection_rule_association" "main" {
  data_collection_rule_id = var.dcr_id
  name                    = "${module.naming.linux_virtual_machine_scale_set.name}-dcr-association"
  # data_collection_endpoint_id = var.dce_id
  target_resource_id = azurerm_orchestrated_virtual_machine_scale_set.main.id
}
