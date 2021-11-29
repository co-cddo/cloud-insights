resource "aws_iam_role" "co-cddo-cloud-insights-role" {
  name = join("", ["co-cddo-cloud-insights-role", (var.role_suffix != "" ? var.role_suffix : "")])
  assume_role_policy = file("${path.module}/client_trust_policy.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}
