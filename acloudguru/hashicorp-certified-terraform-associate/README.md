

### Why ?

- Expand your skills and knownledge about Terraform and best practices
- Solidify T fundamentals

### Terraform init
- download modules and plugins
- sets up the backend for storing T state file, a mechanism by which T tracks resources

### Terraform plan
- Read the code and then creates and shows a "plan" of execution/deployment
- allows the user to "review" the action plan before executing anything
- at this stage, authentication credentials are used to connect to your infrastructure, if required

### Terraform apply
- deployes the instructions and statements in the code
- update the deploymnet state tracking mechanism file, a.k.a. "state file"

### Terraform destroy
- looks at the recorded, stored state file created during deploymnet and destroys all resources created by your code
- should be used with caution, as it is a non-reversible command.

### T code


### T providers
- providers are T's way of abstracting integrations with API control layer of the infrastructure vendors
- providers registry - registry.terraform.io/browse/providers
- providers are plugins. They are released on a separate rhythm from Terraform itself, and each provider has it own series of versions

```
export TF_LOG=trace
```

### T State
- A way for T to keep tabs on what hsa been deployed
- Critical of T functionality
- Stored in flat files
- Helps calculate deployment delta and create new deployment plans
- Never lose your T state file! (?)

### T vars and outputs
- variable validation
  - condition + error_message
- sensitive (don't show during executing)
- base types
  - string, number, bool
  - list, set, map, object, tuple

- output variable values are shown on the shell after running `terraform apply`
- return values that you want to track after a successful T deployment

### T provisioners
- boostrapping custom scripts, commands or actions
- can be run either locally or remotely on resources spun up through the T deployment
- each resource can have its own "provisioner" defining the connection method (ssh, WinRM) and script to execute
  - supports both **ssh** and **winrm** (and only!)
- types: "Creating-time" and "Destroy-time"
- best practices
  - as a last resort
  - they are not tracked by T state files, T cannot track changes
  - only want to invoke actions not covered by T declarative model
  - If exit code != 0, then underlying resource is tainted (resource to be created on next run)
- ${self.id}

# T state
- maps real-world resources to T configration
- prior to any modification operation, T refreshes the state files
- resource dependency metadata is alo tracked via the state file
- helps boost deployment performance by caching resource attributes for subsequent use

CLI:
- utility for manipulating and reading the T state file
- use cases
  - **advanced state management**
  - manually remove a resource from T state file so that it's not managed by T
  - listing out tracked resources and their details (via state and list subcommands)
- common commands
  - `terraform state list`
  - `terraform state rm`
  - `terraform state show`

Remote state storage
- allows sharing state file between distributed teams
- allows locking state so parallel executions don't coincide
- enables sharing "output" values with other T configuration or code

```hcl
terraform {
  backend "s3" {
    region = "us-east-1"
    key    = "tstatefile"
    bucket = "mytstates3bucket55321"
  }
}
```

## T modules

- container for multiple resources that are used together
- root module - consists of code files in your main working directory
- modules can be downloaded or referenced from:
  - T public registry
  - private registry
  - local folder
- module block:
  ```hcl
  module "my-vpc-module" {
    source = "./modules/vpc"
    version = "0.0.5"
    region = var.region
  }
  ```
- take input and provide outputs (`module.my-vpc-module.subnet_id`)

## T built-in functions
UDF not allowed

functions:
- join, file, flatten

```bash
terraform console

max (5,3,1,4,5)

timestamp()
```

## T type constraints

- Primitive - number, string, bool
- Complex - list, tuple, map, object
- Collection - list(type), map(type), set(type)
- Structural - object(type), tuple(type), set(type)
  ```hcl
  variable "instructor" {
    type = object({
      name = string
      age = number
    })
  }
  ```
- Dynamic types - any.
  ```hcl
  variable "data" {
    type = list(any)
    default = [1, 42, 7]
  }
  ```

## T dynamic blocks

Iterate, loop and make code cleaner

supported within the following block types:
- resource
- data
- provider
- provisioner

```hcl
dynamic "ingress" {
  for_each = var.rules
  content {
    from_port = ingress.value["port"]
    to_from = ingress.value["port"]
    protocol = ingress.value["proto"]
    cidr_blocks = ingress.value["cidrs"]
  }
}

variable "rules" {
  default = [
    {
      port = 80
      proto = tcp
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      port = 22
      proto = "tcp"
      cidr_blocks = ["1.2.3.4/32"]
    }
  ]
}
```

## T fmt, taint and import commands

terraform fmt
- formats code for readability
- safe to run at any time

terraform taint
- taints a resource, forcing it to be destroyed and recreated
- modifies the state file, which causes the recreation workflow
- **tainting a source may cause other resources te modified** (which depends on it)
  - e.g. changing PublicIP

For Terraform v0.15.2 and later, the `terraform apply -replace` is recommended; previously terraform taint was used.

terraform import
- maps existing resources to T using an "ID"
- "ID" is dependent on the underlying vendor
- importing the same resource to multiple Terraform resources can cause unknown behavior and **is not recommended**

T configuration block
- https://developer.hashicorp.com/terraform/language/settings
  ```hcl
  terraform {
    required_version = ">=0.13.0"
    ...
  }
  ```

## T Workspaces (CLI)
- The workspaces are alternate state files withing the same working directory
- T starts with a single workspace that is always called `default`. It cannot be deleted
- `terraform workspace new <NAME>`, `terraform workspace select <NAME>`
- Use cases
  - Test changes using a parallel, distinct copy of infrastructure
  - It can be modeled against branches in version control such as Git
- Access to a workspace name is provided through the `${terraform.workspace}` variable

Example:
```hcl
resource "aws_instance" "example" {
  count = terraform.workspace == "default" ? 5 : 1
  # ...
}
```

State files:
- default - `terraform.tfstate`
- others - in folder `terraform.tfstate.d`

## Debugging T

- TF_LOG - env var: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`
- TF_LOG_PATH - by default not defined (disabled)

