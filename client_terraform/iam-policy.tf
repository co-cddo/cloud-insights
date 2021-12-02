resource "aws_iam_policy" "co-cddo-cloud-insights-policy-base" {
  name   = join("", ["co-cddo-cloud-insights-policy-base", (var.policy_suffix != "" ? var.policy_suffix : "")])
  policy = file("${path.module}/client_policy_base.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}

resource "aws_iam_role_policy_attachment" "policy-attach-base" {
  role       = aws_iam_role.co-cddo-cloud-insights-role.name
  policy_arn = aws_iam_policy.co-cddo-cloud-insights-policy-base.arn
}

# create and link the S3 Storage Lens policy if enable_s3_storage_lens is set:

resource "aws_iam_policy" "co-cddo-cloud-insights-policy-s3-storage-lens" {
  count = var.enable_s3_storage_lens ? 1 : 0

  name   = join("", ["co-cddo-cloud-insights-policy-s3-storage-lens", (var.policy_suffix != "" ? var.policy_suffix : "")])
  policy = file("${path.module}/client_policy_s3_storage_lens.json")

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}

resource "aws_iam_role_policy_attachment" "policy-attach-s3" {
  count = var.enable_s3_storage_lens ? 1 : 0

  role       = aws_iam_role.co-cddo-cloud-insights-role.name
  policy_arn = aws_iam_policy.co-cddo-cloud-insights-policy-s3-storage-lens[count.index].arn
}
