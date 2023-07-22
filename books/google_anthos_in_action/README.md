* [Overview of Google Anthos](#overview-of-google-anthos)
  * [Anatomy of a Modern Application](#anatomy-of-a-modern-application)
  * [Accelerating Software Development](#accelerating-software-development)
  * [Standardizing Operations At-Scale](#standardizing-operations-at-scale)
  * [Origins in Google](#origins-in-google)

# Overview of Google Anthos

## Anatomy of a Modern Application
- Modern applications have the property of constantly getting better through frequent updates. On the
  backend these applications often comprise a number of services that are all
  continuously improving
- This approach to writing, updating and deploying applications as ‘microservices’
  that can be used together but also updated, scaled and debugged independently is at the
  heart of modern software development. In this book we refer to this pattern as “Modern” or
  “Cloud Native” application development.
- The  end goal of Application Modernization is typically revenue acceleration

Anthos:
- offers unified local, on-prem and cloud development with event driven automation from source to production.
- gives developers the ability to write code rapidly using modern languages and frameworks with local emulation and test, integrated CI/CD, and supports rapid iteration, experimentation and advanced roll out strategies
- A key goal of the Anthos developer experience is for teams to release code multiple times a day, thereby enhancing both velocity and reliability

## Accelerating Software Development

The innovation process is such that only a few ideas lead to successful new products, most fail and disappear.

Excellence in software development is a hallmark of business success.

Higher velocity means that developers are able to experiment more, test more, and so they come up with a better answer in the same amount of time.

Anthos is the common substrate layer that runs across clouds to provide a common developer experience for accelerating application delivery.

## Standardizing Operations At-Scale

Traditional IT teams have anywhere from 15-30% of their staff in IT operations. This team is not always visibly engaged in new product
introductions with the line-of-business.

Failing to invest in operations automation often means that operations become the bottleneck.

## Origins in Google

At the heart of Anthos is Kubernetes.


# Cloud is a new computing stack

## Summary
- Business are leveraging Public Cloud to meet the demands and agility their businesses require.
- Microservices are becoming more popular in software designs, allowing for parallel development to meet the software requirements without the typical drawbacks of a monolithic architecture.
- Good CI/CD capable of autonomous deployments levergang IaC and automated testing is critical to success.
- Teams are leveraging containers and Kubernetes for the packaging and operation of these applications.
- Google Anthos is filling the void to make Kubernetes a reliable scalable platform for the enterprise.

# Anthos, the one single pane-of-glass

Having an easily understood GUI can help people use the tool more effectively since it lowers the bar for learning the software.

Google Cloud Platform has developed a rich set of dashboards
and integrated tools within the Google Cloud Console to help you monitor, troubleshoot, and
interact with your deployed Anthos clusters

This single pane of glass allows administrators, operations professionals,
developers, and business owners to view the status of their clusters and application
workloads

- Centralization: As the name suggests, a single pane of glass should provide a central UI for resources. admins will be able
  to get a high level view of resources. A central environment should come with its own
  safeguards to avoid any operational compromise.
- Consistency: only focus on Kubernetes
- Ease of use: data coming from different sources are aggregated, normalized and visualized.

Operations Administrator. For Anthos operations, this persona will typically be handling core monitoring and logging, and ensuring the health
of the internal platform built on top of an organization’s infrastructure and cloud environments.

Developers of an organization have important roles to play in deploying and
managing the application their teams are directly responsible for.
Developers are given the tools and responsibility to operate and maintain their own applications, while removing the need for them to manage their
infrastructure directly


For Anthos, we have two types of clusters that are visible in the GUI:
- Attached: clusters are those that are compatible with the
  Connect software, but are not actual GKE clusters
- Anthos-managed: clusters that are
  deployed via Anthos utilities and are a flavor of Google Kubernetes Engine (GKE) in GCP, on-
  premise, or in another cloud

There are some features that are not officially supported on Attached clusters

The solution Google has developed for multi-cluster visibility in Anthos depends on a new
concept called Fleets.

The Anthos dashboard is an enhancement of the existing GKE dashboard.

The Connect framework is new with Anthos and simplifies the
communication process between Google Cloud and clusters located anywhere in the world

Fleets are methods of aggregating clusters together in order to simplify common work
between them.

- Connect. initial connection is outbound, it does not rely on a
  fully routable connection from the cloud to the cluster. This greatly reduces the security
  considerations and does not require the cluster to be discoverable on the public internet.

GCP Console works like proxy between User and Anthos Attached/Managed cluster. TLS certificate + OAuth token.

## The Anthos Cloud UI
### Config Management

Uses git repo as source and Syncing.

## Migrate to containers

One of the major benefits to Anthos is the automatable migration of Windows and Linux VMs
to containers and their deployment onto a compatible Anthos cluster

## Connecting to a Remote cluster
- Amazon EKS
- Microsoft ASK
- Openshift
- Rancher
- KIND

## Summary
- Providing a single pane of glass to hybrid and multi-cloud Kubernetes for any
  organization who uses microservices is a stepping stone to a successful and global
  operation.
- One of the biggest benefits to a single pane of glass is that admins can use the same
  interface to configure service level objectives and alerts to reassure service
  guarantees.
- Anthos UI provides some major advantages including:
  - Central operation of services and resources
  - Consistent operation experience across multiple service providers
  - Effortless navigation and easy staff training
  - Providing a window to any organizational persona
- Anthos UI provides multiple usages including cluster management, service operation
  and observability using a unified interface
- An admin can deploy applications directly from Anthos UI to any registered cluster in
  a few easy steps.

# Anthos, the computing environment built on Kubernetes

While making the installation
easier is a necessary step for most enterprises and frees up time to focus on more important
activities, it does lead to an issue – not understanding the basic components and resources
included in a cluster

In order to use Kubernetes to its full potential, you should understand the
underlying architecture and the role of each component. Knowing how components integrate
with one another and what resources can be used will help you to make good architectural
decisions when deploying a cluster or deploying an application.

## Introducing Physical Servers
- Library / Dependency conflicts between applications
- Difficulty controlling access between multiple teams
- Maintenance windows become difficult to schedule

## Introducing Virtual Machines
- Additional cost of each virtual machine operating system
- Server sprawl - requiring patching and staff to manage each instance
- Difficulty of scaling an application instance out
- Installation of most software requires elevated privileges to be granted to multiple
users

## Containers
a developer now needs to know how to:
- Create a container image
- Maintain different container images
- Use container registries
- Understand the container runtime that is used
- Understand the container orchestrator, e.g. Kubernetes
- Create configuration files for application deployments

## Introduction to Serverless
Serverless abstracts the container from the developer, allowing developers to focus on
their code and image, rather than trying to decide what Kubernetes resources need to be
created to run the application.

## Addressing Kubernetes Gaps

Anthos extends Google’s services and engineering practices to your organization, allowing
you to modernize applications faster with operational consistency across GCP services and
your own environments.

|Anthos Feature|Description|
|---|---|
|Anthos Connect|Connects clusters to GCP, simplifying connectivity, authentication, and authorization of clusters|
|Anthos Config Manager (ACM)|Provides configuration and policy management|
|Anthos Service Mesh (ASM)|Service mesh based on Istio|
|Cloud Operations for GKE|Logging and monitoring|
|Cloud Run|Serverless workloads|
|Istio-Ingress|Ingress controller|

since Anthos runs on a standard
Kubernetes platform, you can replace or add any components that you require

## Managing On-Prem and Off-Prem Clusters

Using the native offering offers the quickest and easiest way to get a new cluster up and
running, since the providers have automated the installation

Using a different solution for multiple installations often lead to a variety of different issues, including:
- Increased staff to support each deployment
- Differences in the deployment of an application for on-prem and off-prem
- Different identity management solutions
- Different Kubernetes versions
- Different security models
- Difficulty in standardizing cluster operations
- No single view for all clusters

Anthos, which addresses the on-prem and
off-prem challenges by providing a Kubernetes installation and management solution that not
only works on GCP and on-premise clusters, but in other Cloud providers like AWS and Azure
running Anthos.

## Kubernetes architecture

When a cluster is running in GCP the control plane is created in a Google managed project, which
limits you from interacting with the admin nodes and the Kubernetes components

