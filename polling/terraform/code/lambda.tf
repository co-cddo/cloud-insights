locals {
  function_name = join("", [
      "cloud-insights-lambda",
      (var.lambda_suffix != "" ? var.lambda_suffix : "")
    ]
  )
}

resource "aws_lambda_function" "lambda" {
  function_name = local.function_name

  memory_size = 1024
  timeout     = 900

  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  role = aws_iam_role.cloud-insights-lambda-role.arn

  handler = "main.lambda_handler"
  runtime = "python3.9"

  environment {
    variables = {
      PRIVATE_BUCKET = local.bucket_private,
      HASH = var.source_code_hash,
      DEBUG = 1
    }
  }

  tags = merge(
    { "Name" : local.function_name },
    var.default_tags,
    var.additional_tags
  )
}
