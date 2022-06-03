# Lab 4 - Add layer of abstractions for environments
We have modularized out template to create reusable components, but whole project (application) should also be versatile enough to be used in multiple environments such as prod, staging, dev or even ephemeral (environment to be spin up when needed and killed after tests are done).

Strategies for multiple environments:
- Using Terraform workspace is possible, but not recommended (this feature allows to have different state files, but does not bring true separation, tights version control of whole project and flexibility to customize and evolve)
- Use separate folder and remote state for each environment
  - This might require to copy your projectcontents between folders not following DRY principle (Do Not Repeat Yourself) - but can be handled with various Git strategies well
  - Use additional tooling to copy things between environments such as Terragrunt
  - Add layer - projects themselves will not store state, but will be referenced as modules and actual state is hold in environments
    - We will use this approach here
    - Projects can be locked to versions in GitHub
    - Two-layers of modules (environmnent -> project "module" -> actual modules with DB etc.) might be little more difficult to understand (not all tooling might be ready, but most is)

In your lab04 folder you will different structure now:
- modules - this contains reusable components (such as Azure SQL in our case)
- projects - this contains projects (eg. application infrastructure) leveraging reusable modules and putting everything together, but with no state
- projects/myproject - project tf files
- projects/myproject/environments - folders containing environments such as prod, staging, dev
- projects/myproject/environments/prod - includes providers configuration and actually holds the state pointing to project as module