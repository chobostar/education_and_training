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


