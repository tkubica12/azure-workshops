locals {
  regions_short = {
    "germanywestcentral"   = "gwc"
    "Germany West Central" = "gwc"
    "swedencentral"        = "sc"
    "Sweden Central"       = "sc"
    "germanynorth"         = "gn"
    "Germany North"        = "gn"
    "polandcentral"        = "pl"
    "Poland Central"       = "pl"
    "westeurope"           = "we"
    "West Europe"          = "we"
    "northeurope"          = "ne"
    "North Europe"         = "ne"
    # Add more mappings as needed
  }

  main_region_short    = lookup(local.regions_short, var.main_region, var.main_region)
  target_region_short  = lookup(local.regions_short, var.target_region, var.target_region)
  storage_region_short = lookup(local.regions_short, var.storage_region, var.storage_region)
}
