output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = aws_api_gateway_rest_api.ecommerce_api.execution_arn
}

output "s3_bucket_name" {
  description = "S3 bucket name for assets"
  value       = aws_s3_bucket.assets.bucket
}

output "dynamodb_tables" {
  description = "DynamoDB table names"
  value = {
    products = aws_dynamodb_table.products.name
    cart     = aws_dynamodb_table.cart.name
    orders   = aws_dynamodb_table.orders.name
  }
}