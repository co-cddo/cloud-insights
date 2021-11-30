variable "default_tags" {
  default = {
    "Service" : "CDDO Cloud Insights",
    "Reference" : "https://github.com/co-cddo/cloud-insights"
  }
  description = "Default resource tags"
  type        = map(string)
}

variable "additional_tags" {
  default     = {}
  description = "Additional resource tags"
  type        = map(string)
}

variable "s3_bucket_suffix" {
  default = ""
  type    = string
}

variable "role_suffix" {
  default = ""
  type    = string
}

variable "policy_suffix" {
  default = ""
  type    = string
}

variable "lambda_suffix" {
  default = ""
  type    = string
}

variable "source_code_hash" {
  default = ""
  type    = string
}
