## CDDO Cloud Insights

The below breaks down the [client_policy_base.json](client_terraform/client_policy_base.json) permissions.

### Organization and Account Read-Only Access

These permissions allow getting _organization_ and account information.

- OrganizationAndAccountReadOnlyAccess
  - account:GetAlternateContact
  - iam:GetAccountPasswordPolicy
  - iam:GetAccountSummary
  - organizations:ListAccounts
  - organizations:ListTagsForResource
  - organizations:DescribeOrganization
  - organizations:DescribeAccount
  - organizations:DescribeOrganizationalUnit
  - organizations:ListAWSServiceAccessForOrganization

### Cost and Billing Read-Only Access

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


### S3 Storage Lens Read-Only

<https://aws.amazon.com/blogs/aws/s3-storage-lens/>

These permissions allow viewing the S3 Storage Lens configuration.

- S3StorageLensReadOnly
  - s3:ListStorageLensConfigurations
  - s3:GetStorageLensConfiguration
  - s3:GetStorageLensConfigurationTagging
