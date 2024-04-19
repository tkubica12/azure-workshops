resource "azapi_resource" "image_template" {
  type      = "Microsoft.VirtualMachineImages/imageTemplates@2022-02-14"
  name      = "nginx-image-template"
  location  = azurerm_resource_group.images.location
  parent_id = azurerm_resource_group.images.id

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  body = jsonencode({
    properties = {
      buildTimeoutInMinutes = 60
      customize = [
        {
          name = "install-nginx"
          type = "Shell"
          inline = [
            "echo \"### Installing services\"\napt update\napt install -y nginx\necho \"### Configuring services\""
          ]
        }
      ]
      distribute = [
        {
          runOutputName     = "runOutputImageVersion"
          type              = "SharedImage"
          galleryImageId    = azurerm_shared_image.nginx.id
          excludeFromLatest = false
          replicationRegions = [
            var.location
          ]
        }
      ]
      source = {
        type      = "PlatformImage"
        publisher = "canonical"
        offer     = "0001-com-ubuntu-server-jammy"
        sku       = "22_04-lts-gen2"
        version   = "latest"
      }
      stagingResourceGroup = azurerm_resource_group.staging.id
      validate = {
        continueDistributeOnFailure = false
        inVMValidations = [
          {
            name = "test-nginx"
            type = "Shell"
            inline = [
              "curl 127.0.0.1"
            ]
          }
        ]
        sourceValidationOnly = false
      }

      vmProfile = {
        osDiskSizeGB           = 32
        userAssignedIdentities = []
        vmSize                 = "Standard_DS1_v2"
        # vnetConfig = {
        #   proxyVmSize = "string"
        #   subnetId    = "string"
        # }
      }
    }
  })

  depends_on = [
    azurerm_role_assignment.image_builder,
    azurerm_role_assignment.image_writer
  ]
}
