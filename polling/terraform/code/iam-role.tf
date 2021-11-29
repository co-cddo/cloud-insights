resource "aws_iam_role" "cloud-insights-lambda-role" {
  name = join("", ["co-cddo-cloud-insights-lambda-role", (var.role_suffix != "" ? var.role_suffix : "")])

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}
