# Professional Cloud Architect Journey

## Reliable Google Cloud Infrastructure: Design and Process 

### Defining Services

Requirements, Analysis and Design
- describe users in terms of roles and personas
  - who
- qualitative requirements with user stories
  - what, why
- quantitative requirements using KPI
  - why
  - time, finance, people 
- use SMART criteria to evaluate your service requirements
  - how
- determine appropriate SLOs and SLIs for your services
  - why, how

Example:
- User story
  - Balance Inquiry
    - SLO
      - Available 99.95%
    - SLI
      - Fraction of 200 vs 500 HTTP responses from API endpoint measured per day
  - Balance Inquire
    - SLO
      - 95% of requests will complete in under 300ms
    - SLI
      - Time to last byte GET requests measured every 10 seconds aggregated per minute

### Microservice Design and Architecture

- Decompose
- Recognize boundaries
- Architect stateful and stateless services to optimize scalability and reliability
- Use 12-factor best practices
- Loosely coupled services by implementing a well-designed REST architecture
- Design consistent, standart RESTful service APIs

Microservice architectures:
- Pros
  - Easier to develope and maintain
  - Redcued risk when deploying new versions
  - Services scale independently to optimize use of infrastructure
  - Faster to innovate and add new features
  - Can use different languages and frameworks for different services
  - Choose the runtime appropriate to each service
- Cons
  - Increased complexity when communicating between services
  - Increased latency across service boundaries
  - Concerns about securing inter-service traffic
  - Multiple deployments
  - Need to ensure that you don't break clients as versions change
  - Must maintain backward compatibility with clients as the microservice evolves

### Designing Reliable Systems 

Key performance metrics:
- Availability
  - fault tolerance
    - avoid single point of failure
    - beware of correlated failures - the group of related items that could fail together is a failure domain
    - avoid cascading failures
    - query of death overload ("business logic error as overconsumption resources")
    - positive feedback cycle overload ("retries overload", intelligence retries - exponential backoff, circuit breaker)
    - lazy deletion to reliably recover when users delete data by mistake
      - user deleted - trash <30 day
      - app delete - soft delete <60 days
      - hard delete 
  - backup
  - health checks
  - clear box metrics
- Durability
  - replication
  - backups
  - practice restore
- Scalability
  - monitor usage
  - use capacity autoscaling

Disaster recovery:
- Cold standby
  - VM snapshots, data backups
  - if main region fails, spin up servers in backup region
  - document and test recovery procedure regularly
- Hot standby
  - Create instance groups in multiple regions
  - Store unstructured data in multi-region buckets
  - For structured data, use a multi-region database such as Spanner or Firestore

Disaster planning:
- Scenario
- Priority
- RPO + RTO
- Backup strategy
- Recovery procedure

### Security

Separation of duties:
- no one person can change or delete data without being detected
- no one person can steal sensitive data
- no one person is in charge of designing, implementing and reporting on sensitive systems

e.g. the people who write the code shouldn't deploy the code, and those who deploy the code shouldn't be able to change it

- Use multiple projects to separate duties
- Different people can be given different rights in different projects
- Use folders to help organize projects

Regularly review audit logs

Securing people:
- Members are identified by their login
- Add members to groups for easier management
- Roles are simply a list of permissions
- Use the Console to easily see what permissions are granted to roles

Securing Machine Access
- ...

Network Security
- Remove external IPs
- Private Google Access
- Configure firewall rules
- Control access to APIs using Cloud Endpoints
- TLS only
- CDN, DDoS prot
- Google Cloud Armor
  - supports layer 7 web application firewall (WAF) rules

Encryption
- GCP provides server-side encryption of data at rest by default
- Data Loss Prevention API can be ised to protect sensitive data by finding it and redacting it
  - scans data in Cloud Storage, Big Query, Firestore
  - detects - emails, credit cards, tax ids


# Developing a Google SRE Culture

[Module 1: Welcome to Developing a Google SRE Culture](https://storage.googleapis.com/cloud-training/C-SRE101-B/M1_%20Introduction%20to%20the%20course.pdf)
[Module 2: DevOps, SRE, and Why They Exist](https://storage.googleapis.com/cloud-training/C-SRE101-B/M2_%20DevOps%2C%20SRE%2C%20and%20Why%20They%20Exist.pdf)
[Module 3: SLOs with Consequences](https://storage.googleapis.com/cloud-training/C-SRE101-B/M3_%20SLOs%20with%20Consequences.pdf)
[Module 4: Make Tomorrow Better than Today](https://storage.googleapis.com/cloud-training/C-SRE101-B/M4_%20Make%20Tomorrow%20Better%20Than%20Today.pdf)
[Module 5: Regulate Workload](https://storage.googleapis.com/cloud-training/C-SRE101-B/M5_%20Regulate%20Workload.pdf)
[Module 6: Apply SRE in Your Organization](https://storage.googleapis.com/cloud-training/C-SRE101-B/M6_Apply%20SRE%20in%20Your%20Organization.pdf)


## Practive exam questions

>Question 3: Incorrect
>You need to set up replication of a 4TB user authentication PostgreSQL database from an on-premises data center to Google Cloud Platform. Large updates are frequently made to the database and private address space communication is required for replication. Which networking solution should you choose?

```
Google Cloud Dedicated Interconnect

Secured, fast connection, hence the choice. This will allow private connection from GCP to the data centre with a fast connection.
```
---
Question 7: Incorrect
You are working with an application development team who believes their current logging tool will not meet their needs for their new cloud-based product. They want a better tool to capture errors and help them analyze their historical log data. What should you do to help them find a solution that meets their needs?

---
Question 9: Incorrect
Your Director of Engineering has mandated that all developers move their development infrastructure resources from on-premises virtual machines to Google Cloud Platform to reduce costs. These resources require state to persist and undergo multiple start/stop events throughout the day. You are tasked with designing the process of running a development environment in Google Cloud while ensuring cost visibility to the finance department.

C is not correct because labels are used to organize instances, not to monitor metrics.

---
Question 17: Incorrect
You are tasked with selecting a suitable storage system for your company's website click data. The data is collected using a custom analytics package and is streamed at a rate of 6,000 clicks per minute, with bursts of up to 8,500 clicks per second. It needs to be stored for future analysis by the data science and user experience teams. Which of the following options should you choose?

Explanation:
- Google Cloud Bigtable is the most suitable option for storing the click-data in this scenario.
- It is designed for handling large amounts of data with high read/write throughput and low latency.
- It is also scalable and can handle bursts of traffic.

Cloud Storage and Cloud Datastore can also store unstructured data, but are not optimized for the high throughput and low latency requirements of click-data.

---
Question 18: Incorrect
How can you optimize ongoing Cloud Storage spend while removing backup files older than 90 days from your backup Cloud Storage bucket?

Explanation:
The best option to remove backup files older than 90 days from a Cloud Storage bucket and optimize ongoing Cloud Storage spend is to write a lifecycle management rule in JSON and push it to the bucket with gsutil.

Cloud Storage's lifecycle management feature allows you to automatically delete old, obsolete objects or move them to different storage classes.

---
Dataproc vs Dataflow

The prime difference between Cloud Dataproc vs Cloud Dataflow is that Dataproc is primarily created for batch processing of large datasets with the help of Hadoop and Spark,
while Dataflow is designed for larger dataset batch processing in real-time with varied data processing techniques such as Apache Beam

---

Question 20: Incorrect
What steps should be taken to improve the performance of a new MySQL database server running on Google Compute Engine, which is used for importing and normalizing performance statistics, with n1-standard-8 virtual machine and 80 GB of SSD persistent disk?

---
Question 26: Incorrect
How can you streamline and expedite the analysis and audit process for reviewing Google Cloud Identity and Access Management (Cloud IAM) policy changes over the previous 12 months?

Enabling Logging export to Google BigQuery allows you to export the audit logs, including the Cloud IAM policy changes, to a BigQuery dataset. By using ACLs (Access Control Lists) and views, you can control and limit the data that is shared with the auditor, ensuring that they only have access to the specific information they require.

Option D (GCS log export) allows you to store the audit logs in a GCS bucket, but it does not provide the same level of queryability and analysis capabilities as BigQuery. 

---
Question 32: Incorrect
Your development team recently installed a new Linux kernel module on the batch servers running on Google Compute Engine (GCE) virtual machines (VMs) to improve the nightly batch process. However, after two days, 50% of the batch servers failed during the nightly batch run. You need to investigate the cause of the failure and collect relevant details to share with the development team. Which three actions should you take? (Choose three.)

Wrong options:
- Option B (Analyzing the GCE Activity log) is not the most appropriate choice because the GCE Activity log primarily captures administrative actions rather than application-level logs or events related to the kernel module or the batch run.
- Option D (Checking live migration events) may not be directly relevant to identifying the cause of the failure unless there are specific indications that live migration events were the root cause.
- Option F (Exporting a debug VM image) may not be necessary in this case as you can gather the required information by accessing the logs and metrics through Stackdriver Logging and the serial console.

---
Question 33: Incorrect
Your company is looking to leverage the cloud for archiving and analyzing log data. They have approximately 100 TB of log data that needs to be stored as a long-term backup while also being available for analytics. Which two steps should you take?

Option D (Insert the log data into Google Cloud Bigtable) is not the ideal choice for this use case. Google Cloud Bigtable is a NoSQL wide-column database primarily designed for high-performance, low-latency workloads. It may not be the most efficient or cost-effective option for log data storage and analysis.

---
Question 35: Incorrect
Your organization wants to maintain independent control over IAM policies for different departments while still having centralized management. Which approach should you choose?

Option A (Multiple Projects within a single Organization) may provide independent control over IAM policies, but it lacks centralized management. Managing separate projects for each department can lead to administrative overhead and potential inconsistencies in policy enforcement.

---

Question 37: Incorrect
As part of implementing their disaster recovery plan, your company is facing latency issues and packet loss while replicating their production MySQL database from their private data center to their GCP project using a Google Cloud VPN connection. What should they do to address this issue?

Unlike a VPN connection, which relies on the public internet and may introduce latency and packet loss, a dedicated interconnect provides a more reliable and consistent network connection.

---

Cloud Dataprep vs Google Cloud Datalab

Cloud Dataprep: Organizations that need an intelligent cloud data service to visually explore, clean, and prepare data for analysis and machine learning

Google Cloud Datalab: Anyone who needs an interactive tool for data exploration, analysis, visualization, and machine learning

---
---
---

The keywords are 1. High-throughput 2. Low latency .  So Dedicated Interconnect is the option.  

---

Predefined dashboards in GCP Cloud Monitoring are useful when you’re getting started or if you want to focus only on the standard metrics provided by Google Cloud for specific Google Cloud services. They offer a quick and easy way to view operational data of your applications without much customization required.

On the other hand, creating custom dashboards is beneficial when you need to monitor specific parts of your application, need more detailed insights, or want to monitor metrics across various services. This is particularly valuable when the predefined dashboards do not provide the exact information you require, or if you need custom views for your monitoring data. These custom dashboards can be shared across your organization to provide specific views for different teams.

---

VPC Service Controls vs Cloud VPN + PGA

Cloud VPN connection to the office network and enabling Private Google Access for on-premises hosts, provides secure connectivity between on-premises resources and Google Cloud but does not solely address preventing access to Cloud Storage buckets from outside the office network.

---

GCP Bucket
Placing a retention policy on a bucket ensures that all current and future objects in the bucket cannot be deleted or replaced until they reach the age you define in the policy

---

Using Cloud Functions to host the APIs allows for a serverless and event-driven approach, where you pay only for the actual invocations and execution time. 

This option leverages the cost efficiency of Cloud Storage, serverless architecture with Cloud Functions, and the scalability of Firestore, making it a suitable choice for a cost-effective web application with occasional traffic spikes. 

---

Serverless VPC access allows your serverless resources, such as App Engine, to connect to resources in a VPC network.

---

By using kubemci (Kubernetes Multi-Cluster Ingress), you can create a global HTTP(s) load balancer that spans both the existing us-central1 cluster and the new asia-southeast1 cluster.

---

VPC Service Controls allow you to define a security perimeter around your Google Cloud resources, including BigQuery.

This helps prevent data exfiltration by enforcing restrictions on data movement within and outside the VPC network. By combining VPC Service Controls with Private Google Access, you can further enhance the security of your environment by ensuring that communication with Google services remains private and within the protected VPC network.

---

Copy VM steps:
1. Create snapshot:
   ```bash
   gcloud compute snapshots create SNAPSHOT_NAME \
    --source-disk SOURCE_DISK \
    --snapshot-type SNAPSHOT_TYPE \
    --source-disk-zone SOURCE_DISK_ZONE
   ```
2. Create a custom image from the snapshot using the following command:
   ```bash
   gcloud compute images create IMAGE_NAME \
    --source-snapshot=SOURCE_SNAPSHOT \
    [--storage-location=LOCATION]
   ```
3. Optional: Share the custom image with users who create VMs in the destination project.
4. In your destination project, create a VM from the custom image using the following command:
   ```bash
   gcloud compute instances create VM_NAME \
    --image-project IMAGE_PROJECT \
    [--image IMAGE | --image-family IMAGE_FAMILY]
    --subnet SUBNET
   ```

