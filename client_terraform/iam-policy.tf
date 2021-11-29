resource "aws_iam_policy" "co-cddo-cloud-insights-policy" {
  name = join("", ["co-cddo-cloud-insights-policy", (var.policy_suffix != "" ? var.policy_suffix : "")])
  policy = file("${path.module}/client_policy.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}

resource "aws_iam_role_policy_attachment" "policy-attach" {
  role       = aws_iam_role.co-cddo-cloud-insights-role.name
  policy_arn = aws_iam_policy.co-cddo-cloud-insights-policy.arn
}
