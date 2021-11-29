provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "cddo-cloud-insights-tfstate"
    key    = "app-prod.tfstate"
    region = "eu-west-2"
  }
}

module "cddo-cloud-insights" {
  source           = "../../code"
  role_suffix      = "-prod"
  policy_suffix    = "-prod"
  lambda_suffix    = "-prod"
  s3_bucket_suffix = "-prod"
  additional_tags  = {
    "Environment": "production"
  }
}
