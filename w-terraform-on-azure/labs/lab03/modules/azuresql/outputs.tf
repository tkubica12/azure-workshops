output "name" {
  value = "${var.prefix}-${random_string.name.result}"
}