
- AWS Storage Gateway is a hybrid cloud storage service that gives you on-premises access to virtually unlimited cloud storage. Customers use Storage Gateway to simplify storage management and reduce costs for key hybrid cloud storage use cases. These include moving backups to the cloud, using on-premises file shares backed by cloud storage, and providing low latency access to data in AWS for on-premises applications.
![](https://d1.awsstatic.com/cloud-storage/product-page-diagram_AWS-Storage-Gateway_HIW%402x.6df96d96cdbaa61ed3ce935262431aabcfb9e52d.png)


- Increase the allocated storage for the DB instance is incorrect. Although this will solve the problem of low disk space, increasing the allocated storage might cause performance degradation during the change.


- ![](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/images/instance_lifecycle.png)


- A gateway endpoint is a gateway that you specify in your route table to access Amazon S3 from your VPC over the AWS network. Interface endpoints extend the functionality of gateway endpoints by using private IP addresses to route requests to Amazon S3 from within your VPC, on-premises, or from a different AWS Region. Interface endpoints are compatible with gateway endpoints. If you have an existing gateway endpoint in the VPC, you can use both types of endpoints in the same VPC.


- the maximum backup retention period for automated backup is only 35 days


- ![](https://d1.awsstatic.com/cloud-storage/File-Gateway-How-it-Works.6a5ce3c54688864e5b951df9cb8732fc4f2926b4.png)


The client that initiates the request chooses the ephemeral port range. The range varies depending on the client's operating system.
- Many Linux kernels (including the Amazon Linux kernel) use ports 32768-61000.
- Requests originating from Elastic Load Balancing use ports 1024-65535.
- Windows operating systems through Windows Server 2003 use ports 1025-5000.
- Windows Server 2008 and later versions use ports 49152-65535.
- A NAT gateway uses ports 1024-65535.
- AWS Lambda functions use ports 1024-65535.
- ![](https://media.tutorialsdojo.com/Network_ACL_Ephemeral_Ports.png)


- ![](https://media.tutorialsdojo.com/instance-store.jpg)


- Expedited retrievals allow you to quickly access your data when occasional urgent requests for a subset of archives are required


- AWS Transit Gateway provides a hub and spoke design for connecting VPCs and on-premises networks. You can attach all your hybrid connectivity (VPN and Direct Connect connections) to a single Transit Gateway consolidating and controlling your organization's entire AWS routing configuration in one place. It also controls how traffic is routed among all the connected spoke networks using route tables.

