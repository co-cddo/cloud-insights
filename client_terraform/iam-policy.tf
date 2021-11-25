resource "aws_iam_role_policy" "cddo-cloud-insights-policy" {
  name = join("", ["cddo-cloud-insights-policy", (var.policy_suffix != "" ? var.policy_suffix : "")])
  role = aws_iam_role.cddo-cloud-insights-role.id

  policy = file("client_policy.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}
