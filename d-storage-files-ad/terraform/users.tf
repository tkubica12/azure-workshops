resource "random_password" "users" {
  length           = 12
  upper            = true
  lower            = true
  numeric          = true
  special          = true
  override_special = "?!"
}

resource "azuread_user" "user1" {
  user_principal_name = "fuser1@tkubica.biz"
  display_name        = "Files User 1"
  password            = random_password.users.result

  depends_on = [
    azurerm_windows_virtual_machine.vm1
  ]
}

resource "azuread_user" "user2" {
  user_principal_name = "fuser2@tkubica.biz"
  display_name        = "Files User 2"
  password            = random_password.users.result

  depends_on = [
    azurerm_windows_virtual_machine.vm2
  ]
}

resource "azuread_user" "admin" {
  user_principal_name = "fadmin@tkubica.biz"
  display_name        = "Files admin"
  password            = random_password.users.result

  depends_on = [
    azurerm_windows_virtual_machine.vm3
  ]
}

resource "azuread_group" "d_storage_files" {
  display_name     = "d-storage-files"
  security_enabled = true
}


resource "azuread_group_member" "user1" {
  group_object_id  = azuread_group.d_storage_files.object_id
  member_object_id = azuread_user.user1.object_id
}

resource "azuread_group_member" "user2" {
  group_object_id  = azuread_group.d_storage_files.object_id
  member_object_id = azuread_user.user2.object_id
}

resource "azuread_group_member" "admin" {
  group_object_id  = azuread_group.d_storage_files.object_id
  member_object_id = azuread_user.admin.object_id
}

resource "azuread_group_member" "dc_user1" {
  group_object_id  = azuread_group.dc_admins.object_id
  member_object_id = azuread_user.user1.object_id
}

resource "azuread_group_member" "dc_user2" {
  group_object_id  = azuread_group.dc_admins.object_id
  member_object_id = azuread_user.user2.object_id
}

resource "azuread_group_member" "dc_fadmin" {
  group_object_id  = azuread_group.dc_admins.object_id
  member_object_id = azuread_user.admin.object_id
}

