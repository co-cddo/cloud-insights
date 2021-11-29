provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "cddo-cloud-insights-tfstate"
    key    = "app-dev.tfstate"
    region = "eu-west-2"
  }
}

module "co-cddo-cloud-insights" {
  source           = "../../code"
  role_suffix      = "-dev"
  policy_suffix    = "-dev"
  lambda_suffix    = "-dev"
  s3_bucket_suffix = "-dev"
  additional_tags  = {
    "Environment": "development"
  }
}
