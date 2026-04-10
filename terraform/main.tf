
data "aws_caller_identity" "current" {}

# ECR repository to store the Lambda container image
resource "aws_ecr_repository" "cli_surf" {
    name                 = "cli-surf"
    image_tag_mutability = "MUTABLE"

    image_scanning_configuration {
        scan_on_push = true
    }
}

# NOTE: The ECR repository policy granting lambda.amazonaws.com access must be set
# manually by an admin (cli-surf IAM user lacks ecr:SetRepositoryPolicy). Run:
#
#   aws ecr set-repository-policy --repository-name cli-surf --region us-west-1 \
#     --policy-text file://ecr-policy.json
#
# where ecr-policy.json grants lambda.amazonaws.com GetDownloadUrlForLayer,
# BatchGetImage, and BatchCheckLayerAvailability.

# Grant Lambda execution role permission to pull from ECR
resource "aws_iam_role_policy" "cli_surf_ecr" {
    name = "cli_surf_ecr_pull"
    role = aws_iam_role.cli_surf_exec.id
    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Effect = "Allow"
            Action = [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetAuthorizationToken"
            ]
            Resource = "*"
        }]
    })
}

# Create HTTP API Gateway
resource "aws_apigatewayv2_api" "http_api" {
    name = "cli-surf-api"
    protocol_type = "HTTP"
}

# connect lambda to API gateway
resource "aws_apigatewayv2_integration" "lambda_integration" {
    api_id = aws_apigatewayv2_api.http_api.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.cli_surf.arn
    payload_format_version  = "2.0"
    timeout_milliseconds    = 29000
}

# Define API route
resource "aws_apigatewayv2_route" "lambda_route" {
    api_id = aws_apigatewayv2_api.http_api.id
    route_key = "$default"
    target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# deploy the API with default stage
resource "aws_apigatewayv2_stage" "default" {
    api_id = aws_apigatewayv2_api.http_api.id
    name = "$default"
    auto_deploy = true

    default_route_settings {
        throttling_rate_limit  = 3
        throttling_burst_limit = 3
    }
}

# grant api gateway permissions to call lambda
resource "aws_lambda_permission" "apigw" {
    statement_id = "AllowAPIGatewayInvoke"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.cli_surf.function_name
    principal = "apigateway.amazonaws.com"
    source_arn = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

resource "aws_iam_role" "cli_surf_exec" {
    name = "cli_surf_exec_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {Service = "lambda.amazonaws.com"}
        }]
    })
}

resource "aws_iam_role_policy_attachment" "cli_surf_basic_execution" {
    role = aws_iam_role.cli_surf_exec.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "cli_surf" {
    function_name = "cli-surf"
    role          = aws_iam_role.cli_surf_exec.arn
    package_type  = "Image"
    image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/cli-surf:latest"

    timeout      = 29
    memory_size  = 512

    depends_on = [aws_ecr_repository.cli_surf, aws_iam_role_policy.cli_surf_ecr]
}
