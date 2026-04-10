
output "api_gateway_invoke_url" {
    value = aws_apigatewayv2_api.http_api.api_endpoint
    description = "Invoke URL of the API Gateway vs HTTP API"
}