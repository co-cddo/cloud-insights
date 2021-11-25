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
