resource "azurerm_databricks_workspace" "main" {
  name                = "databricks"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "trial"

  custom_parameters {
    storage_account_sku_name = "Standard_LRS"
  }
}

resource "databricks_cluster" "shared_cluster" {
  cluster_name            = "Shared cluster"
  spark_version           = "11.3.x-scala2.12"
  node_type_id            = "Standard_D4s_v5"
  autotermination_minutes = 10
  data_security_mode      = "USER_ISOLATION"
  num_workers             = 1

  spark_conf = {
    "spark.databricks.io.cache.enabled" : "true"
  }

  depends_on = [
    azurerm_databricks_workspace.main
  ]
}