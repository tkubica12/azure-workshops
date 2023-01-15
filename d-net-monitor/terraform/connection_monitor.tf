// Monitor connection from VMs to outsite world on http - microsoft.com
resource "azurerm_network_connection_monitor" "http_location1" {
  name               = "http-example-location1"
  network_watcher_id = local.network_watcher_id_location1
  location           = var.location1

  endpoint {
    name               = "vm-location1"
    target_resource_id = azurerm_windows_virtual_machine.vm_location1.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location1.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  endpoint {
    name    = "microsoft-site"
    address = "www.microsoft.com"
  }

  test_configuration {
    name                      = "http-test"
    protocol                  = "Http"
    test_frequency_in_seconds = 60

    success_threshold {
      checks_failed_percent = 5
      round_trip_time_ms    = 250
    }

    http_configuration {
      method                   = "Get"
      port                     = 443
      prefer_https             = false
      valid_status_code_ranges = ["2xx", "3xx"]
    }
  }

  test_group {
    name                     = "http-tests"
    destination_endpoints    = ["microsoft-site"]
    source_endpoints         = ["vm-location1"]
    test_configuration_names = ["http-test"]
  }

  notes = "This will make agent access www.microsoft.com testing all routing towards Internet works fine and site is accessible"

  output_workspace_resource_ids = [azurerm_log_analytics_workspace.main.id]

  depends_on = [azurerm_virtual_machine_extension.location1]
}

resource "azurerm_network_connection_monitor" "http_location2" {
  name               = "http-example-location2"
  network_watcher_id = local.network_watcher_id_location2
  location           = var.location2

  endpoint {
    name               = "vm-location2"
    target_resource_id = azurerm_windows_virtual_machine.vm_location2.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location2.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  endpoint {
    name    = "microsoft-site"
    address = "www.microsoft.com"
  }

  test_configuration {
    name                      = "http-test"
    protocol                  = "Http"
    test_frequency_in_seconds = 60

    success_threshold {
      checks_failed_percent = 5
      round_trip_time_ms    = 250
    }

    http_configuration {
      method                   = "Get"
      port                     = 443
      prefer_https             = false
      valid_status_code_ranges = ["2xx", "3xx"]
    }
  }

  test_group {
    name                     = "http-tests"
    destination_endpoints    = ["microsoft-site"]
    source_endpoints         = ["vm-location2"]
    test_configuration_names = ["http-test"]
  }

  output_workspace_resource_ids = [azurerm_log_analytics_workspace.main.id]

  depends_on = [azurerm_virtual_machine_extension.location2]
}

// Monitor connection from VMs to outsite world on tcp - microsoft.com
resource "azurerm_network_connection_monitor" "tcp_location1" {
  name               = "tcp-example-location1"
  network_watcher_id = local.network_watcher_id_location1
  location           = var.location1

  endpoint {
    name               = "vm-location1"
    target_resource_id = azurerm_windows_virtual_machine.vm_location1.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location1.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  endpoint {
    name    = "microsoft-site"
    address = "www.microsoft.com"
  }

  test_configuration {
    name                      = "tcp-test"
    protocol                  = "Tcp"
    test_frequency_in_seconds = 60

    success_threshold {
      checks_failed_percent = 5
      round_trip_time_ms    = 250
    }

    tcp_configuration {
      port = 80
    }
  }

  test_group {
    name                     = "tcp-tests"
    destination_endpoints    = ["microsoft-site"]
    source_endpoints         = ["vm-location1"]
    test_configuration_names = ["tcp-test"]
  }

  output_workspace_resource_ids = [azurerm_log_analytics_workspace.main.id]

  depends_on = [azurerm_virtual_machine_extension.location1]
}

resource "azurerm_network_connection_monitor" "tcp_location2" {
  name               = "tcp-example-location2"
  network_watcher_id = local.network_watcher_id_location2
  location           = var.location2

  endpoint {
    name               = "vm-location2"
    target_resource_id = azurerm_windows_virtual_machine.vm_location2.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location2.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  endpoint {
    name    = "microsoft-site"
    address = "www.microsoft.com"
  }

  test_configuration {
    name                      = "tcp-test"
    protocol                  = "Tcp"
    test_frequency_in_seconds = 60

    success_threshold {
      checks_failed_percent = 5
      round_trip_time_ms    = 250
    }

    tcp_configuration {
      port = 80
    }
  }

  test_group {
    name                     = "tcp-tests"
    destination_endpoints    = ["microsoft-site"]
    source_endpoints         = ["vm-location2"]
    test_configuration_names = ["tcp-test"]
  }

  output_workspace_resource_ids = [azurerm_log_analytics_workspace.main.id]

  depends_on = [azurerm_virtual_machine_extension.location2]
}

// Monitor connection from VM in location1 to VM in location2
resource "azurerm_network_connection_monitor" "agent2agent" {
  name               = "agent2agent"
  network_watcher_id = local.network_watcher_id_location1
  location           = var.location1

  endpoint {
    name               = "vm-location1"
    target_resource_id = azurerm_windows_virtual_machine.vm_location1.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location1.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  endpoint {
    name               = "vm-location2"
    target_resource_id = azurerm_windows_virtual_machine.vm_location2.id

    filter {
      item {
        address = azurerm_windows_virtual_machine.vm_location2.id
        type    = "AgentAddress"
      }

      type = "Include"
    }
  }

  test_configuration {
    name                      = "agent2agent-test"
    protocol                  = "Tcp"
    test_frequency_in_seconds = 60

    success_threshold {
      checks_failed_percent = 5
      round_trip_time_ms    = 250
    }

    tcp_configuration {
      port                      = 22
      destination_port_behavior = "ListenIfAvailable"
    }
  }

  test_group {
    name                     = "agent2agent-tests"
    destination_endpoints    = ["vm-location2"]
    source_endpoints         = ["vm-location1"]
    test_configuration_names = ["agent2agent-test"]
  }

  output_workspace_resource_ids = [azurerm_log_analytics_workspace.main.id]

  depends_on = [azurerm_virtual_machine_extension.location1, azurerm_virtual_machine_extension.location2]
}
