variable "location" {
  type = string
  default = "northeurope"
  description = <<EOF
The Azure region where the resources will be created.
EOF
}

variable "prefix" {
  type = string
  default = "dex"
  description = <<EOF
A prefix that will be added to the names of the resources.
EOF
}

variable "devbox_image" {
  type = string
  default = "microsoftwindowsdesktop_windows-ent-cpc_win11-23h2-ent-cpc"
  description = <<EOF
The name of the image that will be used to create the devbox.
EOF
}

variable "devbox_size" {
  type = string
  default = "general_i_8c32gb256ssd_v2"
  description = <<EOF
The size of the devbox.
EOF
}
