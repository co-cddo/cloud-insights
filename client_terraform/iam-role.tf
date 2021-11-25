resource "aws_iam_role" "cddo-cloud-insights-role" {
  name = join("", ["cddo-cloud-insights-role", (var.role_suffix != "" ? var.role_suffix : "")])
  assume_role_policy = file("client_trust_policy.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}
