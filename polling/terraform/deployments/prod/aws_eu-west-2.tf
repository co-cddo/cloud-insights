provider "aws" {
  region = "eu-west-2"
}

module "co-cddo-cloud-insights" {
  source           = "../../code"
  role_suffix      = "-prod"
  policy_suffix    = "-prod"
  lambda_suffix    = "-prod"
  s3_bucket_suffix = "-prod"
  additional_tags  = {
    "Environment": "production"
  }
}
