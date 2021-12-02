# Terraform Client

Grant access to AWS billing controls and account and organization information via this Terraform module.

Setting `enable_s3_storage_lens` to `true` enables configuration access to S3 Storage Lens via an additional policy, separate from the read-only base policy.

Module will also be available from S3.

``` tf
module "co-cddo-cloud-insights-access" {
  source = "github.com/co-cddo/cloud-insights//client_terraform?ref=fded14d86d1fa970959cc51744d5a7dfc0e760eb"
  enable_s3_storage_lens = false # default
}

# or from S3 (to be created):

module "co-cddo-cloud-insights-access" {
  source = "s3::https://co-cddo-cloud-insights-public-prod.s3.amazonaws.com/client_cloudformation/client_terraform_0_1.zip"
}

```
