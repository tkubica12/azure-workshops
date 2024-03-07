resource "azapi_resource" "activityLogsToEH" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "activityLogsToEH"
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
  body      = file("${path.module}/policies/test.json")
  # body      = file("${path.module}/policies/activityLogsToEH.json")
}
