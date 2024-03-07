resource "azapi_resource" "initiativeDefenders" {
  type      = "Microsoft.Authorization/policySetDefinitions@2021-06-01"
  name      = "initiativeDefenders"
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
  body      = file("${path.module}/policies/initiativeDefenders.json")
}

