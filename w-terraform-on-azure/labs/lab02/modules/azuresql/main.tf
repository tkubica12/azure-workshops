// Generate random name
resource "random_string" "name" {
  length  = 12
  special = false
  upper   = false
  lower   = true
  number  = false
}
