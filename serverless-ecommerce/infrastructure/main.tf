terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDB Tables
resource "aws_dynamodb_table" "products" {
  name           = "ecommerce-products"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product_id"

  attribute {
    name = "product_id"
    type = "S"
  }

  tags = {
    Name        = "ECommerce Products"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "cart" {
  name           = "ecommerce-cart"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "product_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "product_id"
    type = "S"
  }

  tags = {
    Name        = "ECommerce Cart"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "orders" {
  name           = "ecommerce-orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name     = "UserOrdersIndex"
    hash_key = "user_id"
  }

  tags = {
    Name        = "ECommerce Orders"
    Environment = var.environment
  }
}

# S3 Bucket for static assets
resource "aws_s3_bucket" "assets" {
  bucket = "${var.project_name}-assets-${random_string.bucket_suffix.result}"

  tags = {
    Name        = "ECommerce Assets"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket = aws_s3_bucket.assets.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "assets" {
  bucket = aws_s3_bucket.assets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.assets.arn}/*"
      }
    ]
  })
}

# IAM Role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.products.arn,
          aws_dynamodb_table.cart.arn,
          aws_dynamodb_table.orders.arn,
          "${aws_dynamodb_table.orders.arn}/index/*"
        ]
      }
    ]
  })
}

# API Gateway
resource "aws_api_gateway_rest_api" "ecommerce_api" {
  name        = "${var.project_name}-api"
  description = "Serverless E-Commerce API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# Products Lambda Function
resource "aws_lambda_function" "products" {
  filename         = "products.zip"
  function_name    = "${var.project_name}-products"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  depends_on = [aws_iam_role_policy.lambda_policy]

  tags = {
    Name        = "Products Service"
    Environment = var.environment
  }
}

# Cart Lambda Function
resource "aws_lambda_function" "cart" {
  filename         = "cart.zip"
  function_name    = "${var.project_name}-cart"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  depends_on = [aws_iam_role_policy.lambda_policy]

  tags = {
    Name        = "Cart Service"
    Environment = var.environment
  }
}

# Random string for unique resource names
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "products_logs" {
  name              = "/aws/lambda/${aws_lambda_function.products.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "cart_logs" {
  name              = "/aws/lambda/${aws_lambda_function.cart.function_name}"
  retention_in_days = 14
}