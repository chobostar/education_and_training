

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
