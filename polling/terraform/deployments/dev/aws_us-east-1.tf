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

locals {
  source_files = sort(concat(
    tolist(fileset("", "../../../lambda/*.py")),
    tolist(fileset("", "../../../lambda/*.txt"))
  ))
  source_code_hash = base64sha256(
    join("", [
      for f in local.source_files: filesha256(f)
    ])
  )
}

module "cddo-cloud-insights" {
  source           = "../../code"
  source_code_hash = local.source_code_hash
  role_suffix      = "-dev"
  policy_suffix    = "-dev"
  lambda_suffix    = "-dev"
  s3_bucket_suffix = "-dev"
  additional_tags  = {
    "Environment": "development"
  }
}
