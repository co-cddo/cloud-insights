resource "aws_lambda_function" "lambda" {
  function_name = join("", ["cloud-insights-lambda", (var.lambda_suffix != "" ? var.lambda_suffix : "")])

  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  role = aws_iam_role.cloud-insights-lambda-role.name

  handler = "main.lambda_handler"
  runtime = "python3.9"

  tags = merge(
    var.default_tags,
    var.additional_tags
  )
}
