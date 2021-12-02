## CDDO Cloud Insights

The below breaks down the [client_policy_s3_storage_lens.json](client_terraform/client_policy_s3_storage_lens.json) permissions.

### Enable Storage Lens AWS Organization

This permissions is linked to a
[service-linked role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html)
for S3 Storage Lens (where the below `SetupS3StorageLensServiceLinkedRole` and
`SetupS3StorageLensServiceRolePolicies` allow creating a role scoped to just `storage-lens`).

- EnableStorageLensAWSOrganization
  - organizations:EnableAWSServiceAccess

### Setup S3 Storage Lens Service-Linked Role and Policy

These permissions allow creating a service-linked role for S3 Storage Lens.

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

These permissions allow setting S3 Storage Lens configuration. Storage Lens
allows setting up an S3 bucket as a destination for S3 usage reports. These reports
contain cost, size usage and storage class (e.g.: infrequent access).

- S3StorageLens
  - s3:PutStorageLensConfigurationTagging
  - s3:PutStorageLensConfiguration
