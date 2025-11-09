output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = "https://${aws_api_gateway_rest_api.ecommerce_api.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
}

output "frontend_url" {
  description = "CloudFront distribution URL"
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "s3_frontend_bucket" {
  description = "S3 bucket name for frontend"
  value       = aws_s3_bucket.frontend.bucket
}

output "s3_assets_bucket" {
  description = "S3 bucket name for assets"
  value       = aws_s3_bucket.assets.bucket
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.users.id
}

output "cognito_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.web_client.id
}

output "dynamodb_tables" {
  description = "DynamoDB table names"
  value = {
    products = aws_dynamodb_table.products.name
    cart     = aws_dynamodb_table.cart.name
    orders   = aws_dynamodb_table.orders.name
  }
}