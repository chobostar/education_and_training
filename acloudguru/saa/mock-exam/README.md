A data company has implemented a subscription service for storing video files. There are two levels of subscription: personal and professional use. The personal users can upload a total of 5 GB of data, and professional users can upload as much as 5 TB of data. The application can upload files of size up to 1 TB to an S3 Bucket. What is the best way to upload files of this size?
- Single-part Upload
- Multipart upload
- AWS SnowMobile
- AWS Snowball

QUESTION 2
After an IT Steering Committee meeting you have been put in charge of configuring a hybrid environment for the company’s compute resources. You weigh the pros and cons of various technologies based on the requirements you are given. Your primary requirement is the necessity for a private, dedicated connection, which bypasses the Internet and can provide throughput of 10 Gbps. Which option will you select?
- AWS VPN
- VPC Peering
- AWS Direct Gateway
- AWS Direct Connect


QUESTION 3
An organization of about 100 employees has performed the initial setup of users in IAM. All users except administrators have the same basic privileges. But now it has been determined that 50 employees will have extra restrictions on EC2. They will be unable to launch new instances or alter the state of existing instances. What will be the quickest way to implement these restrictions?
- Create the appropriate policy. With only 20 users, attach the policy to each user.
- Create an IAM Role for the restrictions. Attach it to the EC2 instances.
- Create the appropriate policy. Place the restricted users in the new policy.
- Create the appropriate policy. Create a new group for the restricted users. Place the restricted users in the new group and attach the policy to the group.

QUESTION 4
You have been tasked with designing a strategy for backing up EBS volumes attached to an instance-store-backed EC2 instance. You have been asked for an executive summary on your design, and the executive summary should include an answer to the question, “What can an EBS volume do when snapshotting the volume is in progress”?
- The volume can only accommodate reads while a snapshot is in progress.
- The volume can only accommodate writes while a snapshot is in progress.
- The volume can be used normally while the snapshot is in progress.
- The volume cannot be used while a snapshot is in progress.

QUESTION 5
You have been given an assignment to configure Network ACLs in your VPC. Before configuring the NACLs, you need to understand how the NACLs are evaluated. How are NACL rules evaluated?
- NACL rules are evaluated by rule number from lowest to highest and executed immediately when a matching rule is found.
- All NACL rules that you configure are evaluated before traffic is passed through.
- NACL rules are evaluated by rule number from highest to lowest, and all are evaluated before traffic is passed through.
- NACL rules are evaluated by rule number from highest to lowest, and executed immediately when a matching rule is found.

QUESTION 6
A software company is developing an online "learn a new language" application. The application will be designed to teach up to 20 different languages for native English and Spanish speakers. It should leverage services that are capable of keeping up with 24,000 read units per second and 3,300 write units per second, and scale for spikes and off-peak. The application will also need to store user progress data. Which AWS services would meet these requirements?
- DynamoDB
- RDS
- EBS
- S3

QUESTION 7
You have just started working at a company that is migrating from a physical data center into AWS. Currently, you have 25 TB of data that needs to be moved to an S3 bucket. Your company has just finished setting up a 1 GB Direct Connect drop, but you do not have a VPN currently up and running. This data needs to be encrypted during transit and at rest and must be uploaded to the S3 bucket within 21 days. How can you meet these requirements?
- Upload the data using Direct Connect.
- Use a Snowball device to transmit the data.
- Order a Snowcone device to transmit the data.
- Upload the data to S3 using your public internet connection.

QUESTION 8
Several S3 Buckets have been deleted and a few EC2 instances have been terminated. Which AWS service can you use to determine who took these actions?
- Trusted Advisor
- AWS Inspector
- AWS CloudTrail
- AWS CloudWatch

QUESTION 9
Your company has recently converted to a hybrid cloud environment and will slowly be migrating to a fully AWS cloud environment. The AWS side is in need of some steps to prepare for disaster recovery. A disaster recovery plan needs to be drawn up and disaster recovery drills need to be performed. The company wants to establish Recovery Time and Recovery Point Objectives, with a major component being a very aggressive RTO, with cost not being a major factor. You have determined and will recommend that the best DR configuration to meet cost and RTO/RPO objectives will be to run a second AWS architecture in another Region in an active-active configuration. Which AWS disaster recovery pattern will best meet these requirements?
- Multi-site
- Pilot Light
- Warm Standby
- Backup and restore

QUESTION 10
You are working in a large healthcare facility which uses EBS volumes on most of the EC2 instances. The CFO has approached you about some cost savings and it has been decided that some of the EC2 instances and EBS volumes would be deleted. What step can be taken to preserve the data on the EBS volumes and keep the data available on short notice?
- Move the data to Amazon S3.
- Take point-in-time snapshots of your Amazon EBS volumes.
- Archive the data to Glacier.
- Store the data in CloudFormation user data.

QUESTION 11
A company has created a mobile application that is hugely popular. The initial plan was to give each user login credentials to the application. But due to the volume of users, this idea has become impractical. What service can you use to allow outside users to login through a third party such as Facebook, Amazon, Google or Apple?
- AWS cross account access
- AWS IAM
- Amazon Cognito
- Google Authenticator

QUESTION 12
Recently, you've been experiencing issues with your dynamic application that is running on EC2 instances. These instances aren't able to keep up with the amount of traffic being sent to them, and customers are getting timeouts. Upon further investigation, there is no discernible traffic pattern for these surges. The application can be easily containerized. What can you do to fix the problem while keeping cost in mind?
- Migrate the application to ECS. Use Fargate to run the required tasks.
- Migrate the web application to S3. Enable static website hosting.
- Create a second Auto Scaling group of EC2 instances. When the first is overwhelmed, post the overflow traffic to an SQS queue.
- Increase the minimum and maximum count on the EC2 Auto Scaling group.

QUESTION 13
Your company needs to shift an application to the cloud. You are looking for a solution to collect, process, gain immediate insight, and then transfer the application data to AWS. Part of this effort also includes moving a large data warehouse into AWS. The warehouse is 50TB, and it would take over a month to migrate the data using the current bandwidth available. What is the best option available to perform this one time migration considering both cost and performance aspects?
- AWS Direct Connect
- AWS Snowball Edge
- AWS SnowMobile
- AWS VPN

QUESTION 14
A new startup is considering the advantages of using DynamoDB versus a traditional relational database in AWS RDS. The NoSQL nature of DynamoDB presents a small learning curve to the team members who all have experience with traditional databases. The company will have multiple databases, and the decision will be made on a case-by-case basis. Which of the following use cases would favor DynamoDB? Select THREE.
(Choose 3)
- Storing metadata for S3 objects
- Strong referential integrity between tables
- Managing web session data
- Storing BLOB data
- Storing infrequently accessed data

QUESTION 15
After an IT Steering Committee meeting, you have been put in charge of configuring a hybrid environment for the company’s compute resources. You weigh the pros and cons of various technologies, such as VPN and Direct Connect, and based on the requirements you have decided to configure a VPN connection. What features and advantages can a VPN connection provide?
- It provides a connection between an on-premises network and a VPC, using a secure and private connection with IPsec and TLS.
- It provides a cost-effective, private network connection that bypasses the internet.
- It provides a network connection between two VPCs that can route traffic using IPv4 or IPv6.
- It provides a private, dedicated network connection between an on-premises network and the VPC.

QUESTION 16
An application is hosted on an EC2 instance in a VPC. The instance is in a subnet in the VPC, and the instance has a public IP address. There is also an internet gateway and a security group with the proper ingress configured. But your testers are unable to access the instance from the Internet. What could be the problem?
- Add a route to the route table, from the subnet containing the instance, to the Internet Gateway.
- A virtual private gateway needs to be configured.
- Make sure the instance has a private IP address.
- A NAT gateway needs to be configured.

QUESTION 17
Your company is in the process of creating a multi-region disaster recovery solution for your database, and you have been tasked to implement it. The required RTO is 1 hour, and the RPO is 15 minutes. What steps can you take to ensure these thresholds are met?
- Use RDS to host your database. Enable the Multi-AZ option for your database. In the event of a failure, cut over to the secondary database.
- Use RDS to host your database. Create a cross-region read replica of your database. In the event of a failure, promote the read replica to be a standalone database. Send new reads and writes to this database.
- Take EBS snapshots of the required EC2 instances nightly. In the event of a disaster, restore the snapshots to another region.
- Use Redshift to host your database. Enable "multi-region" failover with Redshift. In the event of a failure, do nothing, as Redshift will handle it for you.

QUESTION 18
The AWS team in a large company is spending a lot of time monitoring EC2 instances and maintenance when the instances report health check failures. How can you most efficiently automate this monitoring and repair?
- Create an Amazon CloudWatch alarm that monitors an Amazon EC2 instance and automatically reboots the instance if a health check fails.
- Create a Lambda function which can be triggered by a failed instance health check. Have the Lambda function deploy a CloudFormation template which can perform the creation of a new instance.
- Create a cron job which monitors the instances periodically and starts a new instance if a health check has failed.
- Create a Lambda function which can be triggered by a failed instance health check. Have the Lambda function destroy the instance and spin up a new instance.

QUESTION 19
You are working as a Solutions Architect for an online travel company. Your application is going to use an Auto Scaling group of EC2 instances but you need to have some decoupling to store messages because of high volume. Which AWS service can be added to the solution to meet this requirement?
- RDS read replicas
- Elasticache
- AWS Simple Workflow Service
- AWS SQS

QUESTION 20
You have been evaluating the NACLs in your company. Most of the NACLs are configured the same:
100 All Traffic Allow
200 All Traffic Deny
* All Traffic Deny
  If a request comes in, how will it be evaluated?
- The default will deny traffic.
- All rules will be evaluated and the end result will be Deny.
- The request will be allowed.
- The highest numbered rule will be used, a deny.

QUESTION 21
A team of architects is designing a new AWS environment for a company which wants to migrate to the Cloud. The architects are considering the use of EC2 instances with instance store volumes. The architects realize that the data on the instance store volumes are ephemeral. Which action will not cause the data to be deleted on an instance store volume?
- Reboot
- Hardware disk failure.
- The underlying disk drive fails.
- Instance is stopped

QUESTION 22
You have joined a newly formed software company as a Solutions Architect. It is a small company, and you are the only employee with AWS experience. The owner has asked for your recommendations to ensure that the AWS resources are deployed to proactively remain within budget. Which AWS service can you use to help ensure you don’t have cost overruns for your AWS resources?
- Billing and Cost Management
- Inspector
- Cost Explorer
- AWS Budgets

QUESTION 23
Your company needs to deploy an application in the company AWS account. The application will reside on EC2 instances in an Auto Scaling Group fronted by an Application Load Balancer. The company has been using Elastic Beanstalk to deploy the application due to limited AWS experience within the organization. The application now needs upgrades and a small team of subcontractors have been hired to perform these upgrades. Which web service can be used to provide users that you authenticate with short-term security credentials that can control access to your AWS resources?
- IAM Group
- IAM user accounts
- AWS SSO
- AWS STS

QUESTION 24
After an IT Steering Committee meeting, you have been put in charge of configuring a hybrid environment for the company’s compute resources. You weigh the pros and cons of various technologies based on the requirements you are given. The decision you make is to go with Direct Connect. Which option best describes the features Direct Connect provides?
- A connection between on-premises and VPC, using secure and private connection with IPsec and TLS
- A private, dedicated network connection between your facilities and AWS
- A cost-effective, private network connection that bypasses the internet
- A network connection between two VPCs that can route traffic using IPv4 or IPv6

QUESTION 25
Several instances you are creating have a specific data requirement. The requirement states that the data on the root device needs to persist independently from the lifetime of the instance. After considering AWS storage options, which is the simplest way to meet these requirements?
- Store your root device data on Amazon EBS and set the DeleteOnTermination attribute to false using a block device mapping.
- Store the data on the local instance store.
- Create a cron job to migrate the data to S3.
- Send the data to S3 using S3 lifecycle rules.

QUESTION 26
A software company has created an application to capture service requests from users and also enhancement requests. The application is deployed on an Auto Scaling Group of EC2 instances fronted by an Application Load Balancer. The Auto Scaling Group has scaled to maximum capacity, but there are still requests being lost. The company has decided to use SQS with the Auto Scaling Group to ensure all messages are saved and processed. What is an appropriate metric for auto scaling with SQS?
- backlog per user
- backlog per hour
- cpu utilization
- backlog per instance

QUESTION 27
A gaming company is designing several new games which focus heavily on player-game interaction. The player makes a certain move and the game has to react very quickly to change the environment based on that move and to present the next decision for the player in real-time. A tool is needed to continuously collect data about player-game interactions and feed the data into the gaming platform in real-time. Which AWS service can best meet this need?
- AWS Lambda
- Kinesis Data Streams
- AWS IoT
- Kinesis Data Analytics

QUESTION 28
You have taken over management of several instances in the company AWS environment. You want to quickly review scripts used to bootstrap the instances at runtime. A URL command can be used to do this. What can you append to the URL http://169.254.169.254/latest/ to retrieve this data?
- meta-data/
- instance-data/
- instance-demographic-data/
- user-data/

QUESTION 29
A testing team is using a group of EC2 instances to run batch, automated tests on an application. The tests run overnight, but don’t take all night. The instances sit idle for long periods of time and accrue unnecessary charges. What can you do to stop these instances when they are idle for long periods?
- Write a Python script which queries the instance status. Also write a Lambda function which can be triggered upon a certain status and stop the instance.
- You can create a CloudWatch alarm that is triggered when the average CPU utilization percentage has been lower than 10 percent for 4 hours, and stops the instance.
- Write a cron job which queries the instance status. Also write a Lambda function which can be triggered upon a certain status and stop the instance.
- Write a cron job which queries the instance status. If a certain status is met, have the cron job kick off CloudFormation to terminate the existing instance, and create a new instance from a template.

QUESTION 30
Your company is using a hybrid configuration because there are some legacy applications which are not easily converted and migrated to AWS. With this configuration comes a typical scenario where the legacy apps must maintain the same private IP address and MAC address. You are attempting to convert the application to the cloud and have configured an EC2 instance to house the application. What you are currently testing is removing the ENI from the legacy instance and attaching it to the EC2 instance. You want to attempt a cold attach. What does this mean?
- Attach ENI when the instance is being launched.
- Attach ENI before the public IP address is assigned.
- Attach ENI when it’s stopped.
- Attach ENI to an instance when it's running.

QUESTION 31
A small startup company has begun using AWS for all of its IT infrastructure. The company has one AWS Solutions Architect and the demands for their time are overwhelming. The software team has been given permission to deploy their Python and PHP applications on their own. They would like to deploy these applications without having to worry about the underlying infrastructure. Which AWS service would they use for deployments?
- CloudFront
- CodeDeploy
- Elastic Beanstalk
- CloudFormation

QUESTION 32
An Application Load Balancer is fronting an Auto Scaling Group of EC2 instances, and the instances are backed by an RDS database. The Auto Scaling Group has been configured to use the Default Termination Policy. You are testing the Auto Scaling Group and have triggered a scale-in. Which instance will be terminated first?
- The instance launched from the oldest launch configuration.
- The instance for which the load balancer stops sending traffic.
- The longest running instance.
- The Auto Scaling Group will randomly select an instance to terminate.

QUESTION 33
You have been evaluating the NACLs in your company. Most of the NACLs are configured the same:
100 All Traffic Allow
200 All Traffic Deny
* All Traffic Deny
  What function does the * All Traffic Deny rule perform?
- Traffic will be denied from specified IP addresses.
- It is there in case no other rules are defined.
- The * specifies that it is an example rule.
- This rule ensures that if a packet doesn't match any of the other numbered rules, it's denied.

QUESTION 34
You have taken over management of several instances in the company AWS environment. You want to quickly retrieve data about the instances such as instance ID, public keys, and public IP address. A URL command can be used to do this. What can you append to the URL http://169.254.169.254/latest/ to retrieve this data?
- meta-data/
- instance-demographic-data/
- user-data/
- instance-data/

QUESTION 35
You are working for a large financial institution and preparing for disaster recovery and upcoming DR drills. A key component in the DR plan will be the database instances and their data. An aggressive Recovery Time Objective (RTO) dictates that the database needs to be synchronously replicated. Which configuration can meet this requirement?
- RDS read replicas
- AWS Lambda triggers a CloudFormation template launch in another Region.
- RDS Multi-AZ
- RDS Multi-Region

QUESTION 36
You are managing S3 buckets in your organization. This management of S3 extends to Amazon Glacier. For auditing purposes you would like to be informed if an object is restored to S3 from Glacier. What is the most efficient way you can do this?
- Create a CloudWatch Event for uploads to S3
- Create a Lambda function which is triggered by restoration of object from Glacier to S3
- Create an SNS notification for any upload to S3
- Configure S3 notifications for restore operations from Glacier

QUESTION 37
You are evaluating the security setting within the main company VPC. There are several NACLs and security groups to evaluate and possibly edit. What is true regarding NACLs and security groups?
- Network ACLs and security groups are both stateless.
- Network ACLs are stateless, and security groups are stateful.
- Network ACLs are stateful, and security groups are stateless.
- Network ACLs and security groups are both stateful.

QUESTION 38
An international travel company has an application which provides travel information and alerts to users all over the world. The application is hosted on groups of EC2 instances in Auto Scaling Groups in multiple AWS Regions. There are also load balancers routing traffic to these instances. In two countries, Ireland and Australia, there are compliance rules in place that dictate users connect to the application in eu-west-1 and ap-southeast-1. Which service can you use to meet this requirement?
- Use Route 53 weighted routing.
- Configure CloudFront and the users will be routed to the nearest edge location.
- Use Route 53 geolocation routing.
- Configure the load balancers to route users to the proper region.

QUESTION 39
A small startup company has begun using AWS for all of its IT infrastructure. The company has two AWS Solutions Architects, and they are very proficient with AWS deployments. They want to choose a deployment service that best meets the given requirements. Those requirements include version control of their infrastructure documentation and granular control of all of the services to be deployed. Which AWS service would best meet these requirements?
- Elastic Beanstalk
- CloudFormation
- Terraform
- OpsWorks

QUESTION 40
A consultant is hired by a small company to configure an AWS environment. The consultant begins working with the VPC and launching EC2 instances within the VPC. The initial instances will be placed in a public subnet. The consultant begins to create security groups. The consultant has launched several instances, created security groups, and has associated security groups with instances. The consultant wants to change the security groups for an instance. Which statement is true?
- You can change the security groups for an instance when the instance is in the running or stopped state.
- You can’t change security groups. Create a new instance and attach the desired security groups.
- You can't change the security groups for an instance when the instance is in the running or stopped state.
- You can change the security groups for an instance when the instance is in the pending or stopped state.

QUESTION 41
A financial institution has begun using AWS services and plans to migrate as much of their IT infrastructure and applications to AWS as possible. The nature of the business dictates that strict compliance practices be in place. The AWS team has configured AWS CloudTrail to help meet compliance requirements and be ready for any upcoming audits. Which item is not a feature of AWS CloudTrail?
- Track changes to resources.
- Answer simple questions about user activity.
- Enables compliance.
- Monitor Auto Scaling Groups and optimize resource utilization.

QUESTION 42
A small startup is beginning to configure IAM for their organization. The user logins have been created and now the focus will shift to the permissions to grant to those users. An admin starts creating identity-based policies. To which item can an identity-based policy not be attached?
- roles
- resources
- groups
- users

QUESTION 43
You work for a large healthcare provider as an AWS lead architect. There is a need to collect data in real-time from devices throughout the organization. The data will include log and event data from sources such as servers, desktops, and mobile devices. The data initially captured will be technical device data, but the goal is to expand the effort to collecting clinical data in real-time from handheld devices used by nurses and doctors. Which AWS service best meets this requirement?
- Kinesis Data Streams
- AWS Lambda
- Kinesis Video Streams
- AWS Redshift

QUESTION 44
You are managing data storage for your company, and there are many EBS volumes. Your management team has given you some new requirements. Certain metrics on the EBS volumes need to be monitored, and the database team needs to be notified by email when certain metric thresholds are exceeded. Which AWS services can be configured to meet these requirements?
(Choose 2)
- SQS
- SNS
- SWF
- SES
- CloudWatch

QUESTION 45
The company you work for has reshuffled teams a bit and you’ve been moved from the AWS IAM team to the AWS Network team. One of your first assignments is to review the subnets in the main VPCs. What are two key concepts regarding subnets?
(Choose 2)
- Private subnets can only hold databases.
- Each subnet is associated with one security group.
- Each subnet maps to a single Availability Zone.
- Every subnet you create is associated with the main route table for the VPC.
- A subnet spans all the Availability Zones in a Region.

QUESTION 46
Your company has gotten back results from an audit. One of the mandates from the audit is that your application, which is hosted on EC2, must encrypt the data before writing this data to storage. Which service could you use to meet this requirement?
- AWS Cloud HSM
- Security Token Service
- AWS KMS
- EBS encryption

QUESTION 47
You have been hired as a Solutions Architect for a company that pairs photos with related story narratives in PDF format. The company needs to be able to store files in several different formats, such as PDF, JPG, PNG, Word, and several others. This storage needs to be highly durable. Which storage type will best meet this requirement?
- DynamoDB
- Amazon RDS
- EC2 instance store
- S3

QUESTION 48
A software company has developed a social gaming application that leverages EC2 web servers with Amazon DynamoDB to store player data, session history, and leaderboards for a huge number of concurrent users. The DynamoDB table has pre-configured read and write capacity units. Users have been reporting slowdown issues, and an analysis has revealed that the application requires response times in microseconds for optimal performance. What step can you take to enable this application to handle read-heavy or bursty workloads, while delivering the fastest possible response time for eventually consistent read operations?
- Add a load balancer in front of the EC2 web servers to decouple your application requests synchronously, improving performance for read-heavy and bursty workloads.
- Configure Amazon SQS to queue requests that could be lost and improve the application response time.
- Deploy Amazon CloudFront to your architecture, so you can cache common Amazon DynamoDB queries and reduce response time to microseconds.
- Implement in-memory acceleration with DynamoDB Accelerator (DAX).

QUESTION 49
Your company is using a hybrid configuration because there are some legacy applications which are not easily converted and migrated to AWS. With this configuration comes a typical scenario where the legacy apps must maintain the same private IP address and MAC address. You are attempting to convert the application to the Cloud and have configured an EC2 instance to house the application. What you are currently testing is removing the ENI from the legacy instance and attaching it to the EC2 instance. You want to attempt a warm attach. What does this mean?
- Attach the ENI before the public IP address is assigned.
- Attach the ENI to an instance when it's running.
- Attach the ENI when the instance is being launched.
- Attach the ENI to an instance when it is stopped.

QUESTION 50
Your company has performed a Disaster Recovery drill which failed to meet the Recovery Time Objective (RTO) desired by executive management. The failure was due in large part to the amount of time taken to restore proper functioning on the database side. You have given management a recommendation of implementing synchronous data replication for the RDS database to help meet the RTO. Which of these options can perform synchronous data replication in RDS?
- Read replicas
- AWS Database Migration Service
- DAX
- RDS Multi-AZ

QUESTION 51
Your company has a small web application hosted on an EC2 instance. The application has just been deployed but no one is able to connect to the web application from a browser. You had recently ssh’d into this EC2 instance to perform a small update, but you also cannot browse to the application from Google Chrome. You have checked and there is an internet gateway attached to the VPC and a route in the route table to the internet gateway. Which situation most likely exists?
- The instance security group has no ingress on port 22 or port 80.
- The instance security group has ingress on port 80 but not port 22.
- The instance security group has ingress on port 22 but not port 80.
- The instance security group has ingress on port 443 but not port 22.

QUESTION 52
You work for an online retailer where any downtime at all can cause a significant loss of revenue. You have architected your application to be deployed on an Auto Scaling Group of EC2 instances behind a load balancer. You have configured and deployed these resources using a CloudFormation template. The Auto Scaling Group is configured with default settings and a simple CPU utilization scaling policy. You have also set up multiple Availability Zones for high availability. The load balancer does health checks against an HTML file generated by script. When you begin performing load testing on your application and notice in CloudWatch that the load balancer is not sending traffic to one of your EC2 instances. What could be the problem?
- The EC2 instance has failed EC2 status checks.
- The EC2 instance has failed the load balancer health check.
- The instance has not been registered with CloudWatch.
- You are load testing at a moderate traffic level and not all instances are needed.

QUESTION 53
You are working for a startup company with a small number of employees. The company expects rapid growth and you have been assigned to configure existing users and onboard new users with IAM privileges and logins. You intend to create IAM groups for the company departments and add new users to the appropriate group when you onboard them. You begin creating policies to assign permissions and attach them to the appropriate group. What is the best practice when giving users permissions in IAM policies?
- Use the principle of top-down privilege.
- Use the principle of least privilege.
- Grant all permissions to each AWS service the user will work with.
- Create a policy for each department head granting root access.

QUESTION 54
Your company has decided to migrate a SQL Server database to a newly-created AWS account. Which service can be used to migrate the database?
- Database Migration Service
- AWS RDS
- Elasticache
- DynamoDB

QUESTION 55
Your boss recently asked you to investigate how to move your containerized application into AWS. During this migration, you'll need to be able to easily move containers back and forth between on-premises and AWS. It has also been requested that you use an open-source container orchestration service. Which AWS tool would you pick to meet these requirements?
- EKS
- EC2 and Docker Swarm
- ECS
- ECR

QUESTION 56
A small startup company has multiple departments with small teams representing each department. They have hired you to configure Identity and Access Management in their AWS account. The team expects to grow rapidly, and promote from within which could mean promoted team members switching over to a new team fairly often. How can you configure IAM to prepare for this type of growth?
- Create the user accounts, create a group for each department, create and attach an appropriate policy to each group, and place each user account into their department’s group. When new team members are onboarded, create their account and put them in the appropriate group. If an existing team member changes departments, move their account to their new IAM group.
- Create the user accounts, create a role for each department, create and attach an appropriate policy to each role, and place each user account into their department’s role. When new team members are onboarded, create their account and put them in the appropriate role. If an existing team member changes departments, move their account to their new IAM group.
- Create the user accounts, create a group for each department, create and attach an appropriate role to each group, and place each user account into their department’s group. When new team members are onboarded, create their account and put them in the appropriate group. If an existing team member changes departments, move their account to their new IAM group.
- Create the user accounts, create a group for each department, create and attach an appropriate policy to each group, and place each user account into their department’s group. When new team members are onboarded, create their account and put them in the appropriate group. If an existing team member changes departments, delete their account, create a new account and put the account in the appropriate group.

QUESTION 57
You work for a Defense contracting company. The company develops software applications which perform intensive calculations in the area of Mechanical Engineering related to metals for ship building. You have a 3-year contract and decide to purchase reserved EC2 instances for a 3-year duration. You are informed that the particular program has been cancelled abruptly and negotiations have brought the contract to an amicable conclusion one year early. What can you do to stop incurring charges and save money on the EC2 instances?
- Write AWS and ask to terminate the contract.
- Change the instance states from running to stopped.
- Sell the reserved instances on the Reserved Instance Marketplace.
- Convert the instances to Spot Instances and allow them to go away through attrition

QUESTION 58
A company needs to deploy EC2 instances to handle overnight batch processing. This includes media transcoding and some voice to text transcription. This is not high priority work, and it is OK if these batch runs get interrupted. What is the best EC2 instance purchasing option for this work?
- Spot
- Dedicated Hosts
- On-Demand
- Reserved

QUESTION 59
An insurance company is creating an application which will perform analytics in near real-time on huge datasets in the terabyte range and potentially even petabyte. The company is evaluating an AWS data storage option. Which AWS service will allow storage of petabyte scale data and also allow fast querying of this data?
- Redshift
- ElastiCache
- DynamoDb
- RDS

QUESTION 60
An international company has many clients around the world. These clients need to transfer gigabytes to terabytes of data quickly and on a regular basis to an S3 bucket. Which S3 feature will enable these long distance data transfers in a secure and fast manner?
- Transfer Acceleration
- Multipart upload
- AWS Snowmobile
- Cross-account replication

QUESTION 61
You have been evaluating the NACLs in your company. Currently, you are looking at the default network ACL. Which statement is true about NACLs?
- The default configuration of the default NACL is Allow, and the default configuration of a custom NACL is Deny.
- The default configuration of the default NACL is Deny, and the default configuration of a custom NACL is Allow.
- The default configuration of the default NACL is Allow, and the default configuration of a custom NACL is Allow.
- The default configuration of the default NACL is Deny, and the default configuration of a custom NACL is Deny.

QUESTION 62
You are designing an architecture which will house an Auto Scaling Group of EC2 instances. The application hosted on the instances is expected to be extremely popular. Forecasts for traffic to this site expect very high traffic and you will need a load balancer to handle tens of millions of requests per second while maintaining high throughput at ultra low latency. You need to select the type of load balancer to front your Auto Scaling Group to meet this high traffic requirement. Which load balancer will you select?
- You will need an Application Load Balancer to meet this requirement.
- You will select a Network Load Balancer to meet this requirement.
- You will need a Classic Load Balancer to meet this requirement.
- All the AWS load balancers meet the requirement and perform the same.

QUESTION 63
A company is going to use several EC2 instances to host various reference applications. The applications are expected to receive steady and relatively low traffic. These applications are expected to run for 3 years, at which time the applications will be evaluated for upgrade. What type of EC2 will meet this requirement considering cost as an additional factor?
- On-Demand
- Spot
- Reserved
- Dedicated Hosts

QUESTION 64
You have been put in charge of S3 buckets for your company. The buckets are separated based on the type of data they are holding and the level of security required for that data. You have several buckets that have data you want to safeguard from accidental deletion. Which configuration will meet this requirement?
- Enable versioning on the bucket and multi-factor authentication delete as well.
- Signed URLs to all users to access the bucket.
- Configure cross-account access with an IAM Role prohibiting object deletion in the bucket.
- Archive sensitive data to Amazon Glacier.

QUESTION 65
An accounting company has big data applications for analyzing actuary data. The company is migrating some of its services to the cloud, and for the foreseeable future, will be operating in a hybrid environment. They need a storage service that provides a simple, scalable, fully managed elastic NFS file system for use with AWS Cloud services and on-premises resources. Which AWS service can meet these requirements?
- EBS
- Glacier
- S3
- EFS

QUESTION 66
A financial institution has an application that produces huge amounts of actuary data, which is ultimately expected to be in the terabyte range. There is a need to run complex analytic queries against terabytes of structured data, using sophisticated query optimization, columnar storage on high-performance storage, and massively parallel query execution. Which service will best meet this requirement?
- RDS
- Redshift
- DynamoDB
- Elasticache

QUESTION 67
You have recently migrated your small company to AWS and are looking for some general best practice guidance within the platform. Which AWS service can help you optimize your AWS environment by giving recommendations to reduce cost, increase performance, and improve security?
- AWS Optimizations
- AWS Organizations
- AWS Trusted Advisor
- AWS Inspector

QUESTION 68
A Solutions Architect has been assigned the task of helping the company development optimize the performance of their web application. End users have been complaining about slow response times. The Solutions Architect has determined that improvements can be realized by adding ElastiCache to the solution. What can ElastiCache do to improve performance?
- Offload some of the write traffic to the database.
- Queue up requests and allow the processor time to catch-up.
- Cache frequently accessed data in-memory.
- Delivers up to 10x performance improvement from milliseconds to microseconds or even at millions of requests per second.

QUESTION 69
Your team has provisioned Auto Scaling groups in a single Region. The Auto Scaling groups, at max capacity, would total 40 EC2 instances between them. However, you notice that the Auto Scaling groups will only scale out to a portion of that number of instances at any one time. What could be the problem?
- You can have only 20 instances per region. This is a hard limit.
- You can have only 20 instances per Availability Zone.
- There is a vCPU-based On-Demand Instance limit per Region.
- The associated load balancer can serve only 20 instances at one time.

QUESTION 70
You have a typical architecture for an Application Load Balancer fronting an Auto Scaling group of EC2 instances, backed by an RDS MySQL database. Your Application Load Balancer is performing health checks on the EC2 instances. What actions will be taken if an instance fails these health checks?
- The ALB notifies the Auto Scaling group that the instance is down.
- The instance is terminated by the ALB.
- The instance is replaced by the ALB.
- The ALB stops sending traffic to the instance.

QUESTION 71
After being assigned to oversee the data storage within your organization, you begin looking at the monthly billing for S3. You notice that large amounts of data are sitting in S3, and after discussions with team members you find that a large amount of the data is historical data that needs to be kept for audit purposes. You detail the cost savings and get approval to move this data to Amazon Glacier for long-term storage. For what types of data is Glacier best suited?
(Choose 2)
- Cached data
- Archival data
- Infrequently accessed data
- Relational table data

QUESTION 72
You work for an advertising company that has a real-time bidding application. You are also using CloudFront on the front end to accommodate a worldwide user base. Your users begin complaining about response times and pauses in real-time bidding. What is the best service that can be used to reduce DynamoDB response times by an order of magnitude (milliseconds to microseconds)?
- DAX
- CloudFront Edge Caches
- DynamoDB Auto Scaling
- ElastiCache