# Crossplane vs Terraform

https://blog.crossplane.io/crossplane-vs-terraform/

There are parallels between the two projects:
- Both allow engineers to **model their infrastructure as declarative configuration**
- Both support managing a myriad of diverse infrastructure using "provider" plugins (extensibility)
- Both are open source tools with strong communities

The key difference is that **Crossplane is a control plane**, 
where Terraform is a command-line tool - an interface to control planes

## Collaboration

Terraform recommends breaking a monolithic configuration up into increasingly more granular configurations. It can require a lot of refactoring over time.

In Crossplane every piece of infrastructure is an API endpoint that supports create, read, update, and delete operations. Crossplane does not need to calculate a graph of dependencies to make a change, so you can easily operate on a single database, even if you manage your entire production environment with Crossplane.

* (спорно, т.к. "строгость" это про консистентность, а "свобода" это значит - кто-то другой должен выполнять эту ответственность. Похоже на SQL vs Schemaless).

## Self Service

Modern organisations are evolving from centralised management of infrastructure to a self service model in which an operations team - often called a platform team.

Terraform module provides a simplified abstraction atop a broader configuration of external resources - for example [the RDS module](https://registry.terraform.io/modules/terraform-aws-modules/rds/aws/latest) abstracts eight distinct Terraform resources into a single “RDS instance” concept.

The Crossplane equivalent of a Terraform module is a Composite Resource - an XR.

## Integration and Automation

Terraform (CLI) is typically invoked only when an engineer expects that infrastructure needs updating. Configuration drift.

Crossplane constantly observes and corrects an infrastructure to match its desired configuration whether changes are expected or not.

* (т.е. crossplane моментально наказывает за внешнее вмешательство)

## Why Not Both?

Terraform is an interface to control planes, and its Kubernetes provider allows to orchestrate the Kubernetes control plane! This means it’s possible to pair Terraform with Crossplane, for example if your organisation prefers HCL to YAML its possible for your platform team to use Terraform to define XRs and Compositions, and for your application teams use Terraform to plan and and apply changes to Crossplane’s desired state!

* (однако не надо так делать - Argo CD, Flux CD or any GitOps tools are much better than Terraform.)
