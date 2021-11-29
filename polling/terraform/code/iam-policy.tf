resource "aws_iam_policy" "cloud-insights-lambda-policy" {
  name = join("", ["cloud-insights-lambda-policy", (var.policy_suffix != "" ? var.policy_suffix : "")])

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:iam::*:role/co-cddo-cloud-insights-role*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action = [
          "s3:Get*",
          "s3:Put*",
          "s3:List*"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${local.bucket_private}/",
          "arn:aws:s3:::${local.bucket_private}/*",
        ]
      }
    ]
  })

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}

resource "aws_iam_role_policy_attachment" "policy-attach" {
  role       = aws_iam_role.cloud-insights-lambda-role.name
  policy_arn = aws_iam_policy.cloud-insights-lambda-policy.arn
}
