locals {
  bucket_private = join("", [
      "co-cddo-cloud-insights-private",
      (var.s3_bucket_suffix != "" ? var.s3_bucket_suffix : "")
    ]
  )
}

resource "aws_s3_bucket" "private-bucket" {
  bucket = local.bucket_private

  versioning {
    enabled    = true
  }

  tags = merge(
    { "Name" : local.bucket_private },
    var.default_tags,
    var.additional_tags
  )
}
