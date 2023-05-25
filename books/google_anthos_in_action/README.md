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

(Здесь прочитать внимательно как Anthos авторизуется в удаленном кластере, пока видно что через service account) 

