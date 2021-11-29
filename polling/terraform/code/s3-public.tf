locals {
  bucket = join("", [
      "co-cddo-cloud-insights-public",
      (var.s3_bucket_suffix != "" ? var.s3_bucket_suffix : "")
    ]
  )
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = local.bucket

  versioning {
    enabled    = true
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicRead",
        Action    = ["s3:GetObject", "s3:ListBucket", "s3:GetObjectVersion"]
        Resource  = [
          "arn:aws:s3:::${local.bucket}/*",
          "arn:aws:s3:::${local.bucket}"
        ]
        Effect    = "Allow"
        Principal = "*"
      }
    ]
  })

  tags = merge(
    { "Name" : local.bucket },
    var.default_tags,
    var.additional_tags
  )
}
