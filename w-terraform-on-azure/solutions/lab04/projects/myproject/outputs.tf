output "sqlNames" {
  value = values(module.sql)[*].name
}