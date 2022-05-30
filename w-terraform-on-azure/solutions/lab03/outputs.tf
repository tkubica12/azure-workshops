output "sqlNames" {
  value = values(module.sql)[*].name
}

output "databases" {
  value = yamlencode(local.databases)
}