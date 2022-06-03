# Reference project here
# Note we are using relative path now,
# which is good for trunk-based development.
# Latest template should be in our staging.
# For production we will use explicit versioning 
# so change in project definition 
# does not accidentally affect production.

module "myproject" {
  source            = "../../"
  resoucreGroupName = "lab04-staging"
  databases         = yamldecode(file("databases.yaml"))["databases"]
}
