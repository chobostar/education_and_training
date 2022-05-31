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
