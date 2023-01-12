resource "azurerm_machine_learning_compute_instance" "demo" {
  count                         = var.deploy_managed_instance ? 1 : 0
  name                          = "demo"
  location                      = azurerm_resource_group.demo.location
  machine_learning_workspace_id = azurerm_machine_learning_workspace.demo.id
  virtual_machine_size          = "Standard_D2as_v4"
  authorization_type            = "personal"
  local_auth_enabled            = false

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aml.id,
    ]
  }
}

resource "azurerm_machine_learning_compute_cluster" "demo" {
  count                         = var.deploy_managed_cluster ? 1 : 0
  name                          = "managed-cluster"
  location                      = azurerm_resource_group.demo.location
  vm_priority                   = "Dedicated"
  vm_size                       = "STANDARD_D2A_V4"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.demo.id
  ssh_public_access_enabled     = true
  local_auth_enabled            = true

  ssh {
    admin_username = "tomas"
    admin_password = "Azure12345678"
    key_value      = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNN/xTE/WrpgK5nROtHupBqlHHVXQAP3c2wcvDz8PO/xLIawd8bPtrbKTmJX3TEVYe+WwQAc5K2XZrzaVGmiZeZSsHhiG3lX9kh2BbxZ9WLtLwta5gmkby4HTdk4sD3yeFFfrrdqHip5+DGl/OijUZC4ihMV6bS9P8jmugxtQKMkIeUC41HaShkXM44rnTRAvQoDr9iJZrAuuKDIZwhIv3ax8J0eu8WaRAVa5t8uZjL2Tv2QmMyK4oZtj89aVsSQyn26T3omNXfJVC/0kltM/Iu3jYXoRZz+8zAOhpTk4C6IsquM0FYsjkNBiip7/9rQCVArNMK6/Hojdl04UvVbi/QZRh4wAc9Ii49ZvD6bIxa0fc3uNl0I/EHN+BknkfzyKXuZ31roTn6xtWLcGrNN9zU+pX9Y69BvRaz2rIeYTGkQ//N7XZRV+Iv4cCEOwOrDxA61xcNDQVMLzW79Q1gQp2vD5Mybn0/LD5hb1TlAxkJfZXfdabDh/BnEEOuZFZLrgMU4c39OeQMWMV/c1gctytmLiIg4LcjhLzyzYwAShFwo+Ajkb46GWyYJD5tVnaqtf5AC6oY6C0linO6UbmpBqoWuUvM+Z6biTEP+qrUhxQ+4XVC4DwPz9Tf+YuKRvxMS5bhVxEcAFdwi1NAwfOXRMNdHRp730uslHz69gR9s3pIw=="
  }

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 10
    scale_down_nodes_after_idle_duration = "PT30M"
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aml.id,
    ]
  }

  lifecycle {
    ignore_changes = [
      ssh[0].admin_password
    ]
  }
}

resource "azurerm_machine_learning_compute_cluster" "gpu" {
  count                         = var.deploy_managed_gpu_cluster ? 1 : 0
  name                          = "gpu-cluster"
  location                      = azurerm_resource_group.demo.location
  vm_priority                   = "Dedicated"
  vm_size                       = "STANDARD_NC6"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.demo.id
  ssh_public_access_enabled     = true
  local_auth_enabled            = true

  ssh {
    admin_username = "tomas"
    admin_password = "Azure12345678"
    key_value      = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNN/xTE/WrpgK5nROtHupBqlHHVXQAP3c2wcvDz8PO/xLIawd8bPtrbKTmJX3TEVYe+WwQAc5K2XZrzaVGmiZeZSsHhiG3lX9kh2BbxZ9WLtLwta5gmkby4HTdk4sD3yeFFfrrdqHip5+DGl/OijUZC4ihMV6bS9P8jmugxtQKMkIeUC41HaShkXM44rnTRAvQoDr9iJZrAuuKDIZwhIv3ax8J0eu8WaRAVa5t8uZjL2Tv2QmMyK4oZtj89aVsSQyn26T3omNXfJVC/0kltM/Iu3jYXoRZz+8zAOhpTk4C6IsquM0FYsjkNBiip7/9rQCVArNMK6/Hojdl04UvVbi/QZRh4wAc9Ii49ZvD6bIxa0fc3uNl0I/EHN+BknkfzyKXuZ31roTn6xtWLcGrNN9zU+pX9Y69BvRaz2rIeYTGkQ//N7XZRV+Iv4cCEOwOrDxA61xcNDQVMLzW79Q1gQp2vD5Mybn0/LD5hb1TlAxkJfZXfdabDh/BnEEOuZFZLrgMU4c39OeQMWMV/c1gctytmLiIg4LcjhLzyzYwAShFwo+Ajkb46GWyYJD5tVnaqtf5AC6oY6C0linO6UbmpBqoWuUvM+Z6biTEP+qrUhxQ+4XVC4DwPz9Tf+YuKRvxMS5bhVxEcAFdwi1NAwfOXRMNdHRp730uslHz69gR9s3pIw=="
  }

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 10
    scale_down_nodes_after_idle_duration = "PT2M"
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aml.id,
    ]
  }

  lifecycle {
    ignore_changes = [
      ssh[0].admin_password
    ]
  }
}

resource "azurerm_machine_learning_compute_cluster" "gpu_spot" {
  count                         = var.deploy_managed_gpu_cluster ? 1 : 0
  name                          = "gpu-spot-cluster"
  location                      = azurerm_resource_group.demo.location
  vm_priority                   = "LowPriority"
  vm_size                       = "STANDARD_NC6S_V3"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.demo.id
  ssh_public_access_enabled     = true
  local_auth_enabled            = true

  ssh {
    admin_username = "tomas"
    admin_password = "Azure12345678"
    key_value      = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNN/xTE/WrpgK5nROtHupBqlHHVXQAP3c2wcvDz8PO/xLIawd8bPtrbKTmJX3TEVYe+WwQAc5K2XZrzaVGmiZeZSsHhiG3lX9kh2BbxZ9WLtLwta5gmkby4HTdk4sD3yeFFfrrdqHip5+DGl/OijUZC4ihMV6bS9P8jmugxtQKMkIeUC41HaShkXM44rnTRAvQoDr9iJZrAuuKDIZwhIv3ax8J0eu8WaRAVa5t8uZjL2Tv2QmMyK4oZtj89aVsSQyn26T3omNXfJVC/0kltM/Iu3jYXoRZz+8zAOhpTk4C6IsquM0FYsjkNBiip7/9rQCVArNMK6/Hojdl04UvVbi/QZRh4wAc9Ii49ZvD6bIxa0fc3uNl0I/EHN+BknkfzyKXuZ31roTn6xtWLcGrNN9zU+pX9Y69BvRaz2rIeYTGkQ//N7XZRV+Iv4cCEOwOrDxA61xcNDQVMLzW79Q1gQp2vD5Mybn0/LD5hb1TlAxkJfZXfdabDh/BnEEOuZFZLrgMU4c39OeQMWMV/c1gctytmLiIg4LcjhLzyzYwAShFwo+Ajkb46GWyYJD5tVnaqtf5AC6oY6C0linO6UbmpBqoWuUvM+Z6biTEP+qrUhxQ+4XVC4DwPz9Tf+YuKRvxMS5bhVxEcAFdwi1NAwfOXRMNdHRp730uslHz69gR9s3pIw=="
  }

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 20
    scale_down_nodes_after_idle_duration = "PT2M"
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aml.id,
    ]
  }

  lifecycle {
    ignore_changes = [
      ssh[0].admin_password
    ]
  }
}
