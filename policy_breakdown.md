## CDDO Cloud Insights

The below breaks down the [client_policy.json](client_terraform/client_policy.json) permissions.

### Organization and Account Access

These permissions allow getting _organization_ and account information.

Additionally, the `organizations:ListAWSServiceAccessForOrganization` and
`organizations:EnableAWSServiceAccess` permissions are linked to a
[service-linked role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html)
for S3 Storage Lens (where the below `SetupS3StorageLensServiceLinkedRole` and
`SetupS3StorageLensServiceRole` allow creating a role scoped to just `storage-lens`).

- OrganizationAndAccountAccess
  - account:GetAlternateContact
  - iam:GetAccountPasswordPolicy
  - iam:GetAccountSummary
  - organizations:ListAccounts
  - organizations:ListTagsForResource
  - organizations:DescribeOrganization
  - organizations:DescribeAccount
  - organizations:DescribeOrganizationalUnit
  - organizations:ListAWSServiceAccessForOrganization
  - organizations:EnableAWSServiceAccess

### Cost and Billing Access

These permissions allow viewing and getting billing, cost and usage information.

* cur == Cost and Usage Reports
* ce == Cost Explorer

- CostAndBillingAccess
  - aws-portal:ViewPaymentMethods
  - aws-portal:ViewAccount
  - aws-portal:ViewBilling
  - aws-portal:ViewUsage
  - cur:DescribeReportDefinitions 
  - ce:List*
  - ce:Describe*
  - ce:Get*

### Setup S3 Storage Lens Service-Linked Role and Policy

These permissions allow viewing and getting billing, cost and usage information.

- SetupS3StorageLensServiceLinkedRole
  - iam:CreateServiceLinkedRole
    - Resource: "arn:aws:iam::*:role/aws-service-role/storage-lens.s3.amazonaws.com/*"
    - Condition: {"StringLike": {"iam:AWSServiceName": "storage-lens.s3.amazonaws.com"}}

- SetupS3StorageLensServiceRole
  - iam:AttachRolePolicy
  - iam:PutRolePolicy
    - Resource: "arn:aws:iam::*:role/aws-service-role/storage-lens.s3.amazonaws.com/*"

### S3 Storage Lens

<https://aws.amazon.com/blogs/aws/s3-storage-lens/>

These permissions allow viewing and setting S3 Storage Lens configuration. Storage Lens 
allows setting up an S3 bucket as a destination for S3 usage reports. These reports
contain cost, size usage and storage class (e.g.: infrequent access).

- S3StorageLens
  - s3:ListStorageLensConfigurations
  - s3:GetStorageLensConfiguration
  - s3:GetStorageLensConfigurationTagging
  - s3:PutStorageLensConfigurationTagging
  - s3:PutStorageLensConfiguration
