# AWS Certified Solutions Architect - Associate (SAA-C02)

- https://aws.amazon.com/architecture/
- https://aws.amazon.com/architecture/well-architected/
- https://aws.amazon.com/blogs/architecture/

## AWS Fundamentals

3 tips for AWS building blocks:
- A region (physical location in the world that consist of two or more AZ)
- An AZ - one or more discrete DC
- Edge locations - endpoints for AWS that are used for caching content. CDN

Responsibilities:
- If you can do it yourself - you are likely responsible:
  - SG, IAM users, patching EC2 OS etc
- If not, AWS is likely responsible
  - Management of DC, security cameras, cabling, patching RDS OS etc
- Encryption is a shared responsibility

Key Services:
- Compute: EC2, Lambda, Elastic Beanstalk
- Storage: S3, EBS, EFS, FSx, Storage Gateway
- Databases: RDS, DynamoDB, Redshift
- Networking: VPCs, Direct Connect, Route 53, API Gateway, AWS Global Accelerator


### IAM

4 steps to secure AWS Root Account:
- enable multi-factor authentication on the root account
- create ad admin group for your administrators, and assign the appropriate permissions to this group
- create user accounts for your administrators
- add your users to the admin group

IAM is Universal: It does not apply to regions at this time.

The Root Account: This is the account created when you first set up your AWS account and it has complete admin access. Secure it as soon as possible and do not use it log in day to day.

New Users: No permissions when first created

Access key ID and secret access keys - for APIs and CLI. Only regenerate them in case of losing.

Always set up password rotations.

IAM Federation: You can combine your existings user account with AWS. For example the same credentials as AD.

Identity Federation: Uses the SAML standart, which is AD

### Simple Storage Service

- object based - allows you to upload files
- files up to 5TB - from 0 to 5 TB
- not OS or DB Storage - not suitable to install an operating system or run database on
- unlimited storage - the total volume of data and the number of objects you can store is unlimited

S3 is a universal namespace. Successful CLI or API uploads will generate an HTTP 200 status code.
- Key - object name
- Value - the data itself, sequence of bytes
- Version ID - allow to store multiple versions of the same object
  - Cannot Be Disabled - once enables, only suspended
- Metadata - data about the you are storing - content-type, last-modified, etc

- Buckets are private by default
- Objects ACL - you can make individual objects public using object ACLs
- Bucket policies. You can make entire buckets public using bucket policies.
- HTTP status code. When you upload an object to S3 and it's successful, you receive HTTP 200
- Static Content - for static website
- Automatic Scaling - S3 Scales automatically with demand

Lifecycle management with S3:
- Automates moving your objects between the different storage tiers
- Can be used in conjuction with versioning
- Can be applied to current versions and previous versions

S3 Object Lock - to store objects using a write once, read many model. Can be on indovodual objects or applied across the bucket as a whole.

Prefix - folders and subfolders.
- 3.5k PUT/COPY/POST/DELETE and 5.5K GET/HEAD RPS per prefix
- better performance by spreading your reads across different prefixes. eg. 2 prefixes == 11k RPS

Multiparts:
- Should be used for any files >100MB
- Must be used for >5GB

Replication:
- between buckets
- existing objects are not replicatd automatically
- delete markers are not replicated by default

Links:
- https://aws.amazon.com/s3/storage-classes/
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html