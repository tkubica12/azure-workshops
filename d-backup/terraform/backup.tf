resource "azurerm_data_protection_backup_vault" "vaulted" {
  name                = "backup-vaulted"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  datastore_type      = "VaultStore"
  redundancy          = "GeoRedundant"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_recovery_services_vault" "vaulted" {
  name                         = "recovery-vault"
  location                     = azurerm_resource_group.main.location
  resource_group_name          = azurerm_resource_group.main.name
  sku                          = "Standard"
  storage_mode_type            = "ZoneRedundant"
  cross_region_restore_enabled = false
  soft_delete_enabled          = true
}

resource "azapi_resource" "blob_backup_policy" {
  type      = "Microsoft.DataProtection/backupVaults/backupPolicies@2022-11-01-preview"
  name      = "blob-backup-policy"
  parent_id = azurerm_data_protection_backup_vault.vaulted.id

  body = jsonencode({
    properties = {
      datasourceTypes = [
        "Microsoft.Storage/storageAccounts/blobServices"
      ]
      objectType = "BackupPolicy"
      "policyRules" : [
        {
          "lifecycles" : [
            {
              "deleteAfter" : {
                "objectType" : "AbsoluteDeleteOption",
                "duration" : "P7D"
              },
              "targetDataStoreCopySettings" : [],
              "sourceDataStore" : {
                "dataStoreType" : "OperationalStore",
                "objectType" : "DataStoreInfoBase"
              }
            }
          ],
          "isDefault" : true,
          "name" : "Default",
          "objectType" : "AzureRetentionRule"
        },
        {
          "lifecycles" : [
            {
              "deleteAfter" : {
                "objectType" : "AbsoluteDeleteOption",
                "duration" : "P7D"
              },
              "targetDataStoreCopySettings" : [],
              "sourceDataStore" : {
                "dataStoreType" : "VaultStore",
                "objectType" : "DataStoreInfoBase"
              }
            }
          ],
          "isDefault" : true,
          "name" : "Default",
          "objectType" : "AzureRetentionRule"
        },
        {
          "backupParameters" : {
            "backupType" : "Discrete",
            "objectType" : "AzureBackupParams"
          },
          "trigger" : {
            "schedule" : {
              "repeatingTimeIntervals" : [
                "R/2023-03-21T15:30:00+00:00/P1D"
              ],
              "timeZone" : "UTC"
            },
            "taggingCriteria" : [
              {
                "tagInfo" : {
                  "tagName" : "Default"
                },
                "taggingPriority" : 99,
                "isDefault" : true
              }
            ],
            "objectType" : "ScheduleBasedTriggerContext"
          },
          "dataStore" : {
            "dataStoreType" : "VaultStore",
            "objectType" : "DataStoreInfoBase"
          },
          "name" : "BackupDaily",
          "objectType" : "AzureBackupRule"
        }
      ]
    }
  })
}


resource "azurerm_data_protection_backup_instance_blob_storage" "blob_backup" {
  name               = "blob-backup-instance"
  vault_id           = azurerm_data_protection_backup_vault.vaulted.id
  location           = azurerm_resource_group.main.location
  storage_account_id = azurerm_storage_account.main.id
  backup_policy_id   = azapi_resource.blob_backup_policy.id

  depends_on = [azurerm_role_assignment.vaulted]
}

resource "azurerm_backup_container_storage_account" "files_protection_container" {
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vaulted.name
  storage_account_id  = azurerm_storage_account.main.id
}

resource "azurerm_backup_policy_file_share" "main" {
  name                = "files-backup-policy"
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vaulted.name

  backup {
    frequency = "Daily"
    time      = "23:00"
  }

  retention_daily {
    count = 7
  }
}

resource "azurerm_backup_protected_file_share" "share1" {
  resource_group_name       = azurerm_resource_group.main.name
  recovery_vault_name       = azurerm_recovery_services_vault.vaulted.name
  source_storage_account_id = azurerm_storage_account.main.id
  source_file_share_name    = azurerm_storage_share.main.name
  backup_policy_id          = azurerm_backup_policy_file_share.main.id
}
