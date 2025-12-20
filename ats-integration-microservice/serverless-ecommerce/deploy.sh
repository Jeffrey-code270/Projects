#!/bin/bash
# Serverless E-Commerce Deployment Script

set -e

echo "🚀 Deploying Serverless E-Commerce Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI not found. Please install AWS CLI.${NC}"
        exit 1
    fi
    
    if ! command -v terraform &> /dev/null; then
        echo -e "${RED}Terraform not found. Please install Terraform.${NC}"
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}AWS credentials not configured. Please run 'aws configure'.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
}

# Package Lambda functions
package_lambdas() {
    echo -e "${YELLOW}📦 Packaging Lambda functions...${NC}"
    
    cd backend/products
    zip -r ../../infrastructure/products.zip . -x "*.pyc" "__pycache__/*"
    
    cd ../cart
    zip -r ../../infrastructure/cart.zip . -x "*.pyc" "__pycache__/*"
    
    cd ../../
    echo -e "${GREEN}✅ Lambda functions packaged${NC}"
}

# Deploy infrastructure
deploy_infrastructure() {
    echo -e "${YELLOW}🏗️ Deploying infrastructure...${NC}"
    
    cd infrastructure
    terraform init
    terraform plan
    terraform apply -auto-approve
    
    cd ../
    echo -e "${GREEN}✅ Infrastructure deployed${NC}"
}

# Seed sample data
seed_data() {
    echo -e "${YELLOW}🌱 Seeding sample data...${NC}"
    
    python3 -c "
import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ecommerce-products')

sample_products = [
    {
        'product_id': 'prod-001',
        'name': 'Wireless Headphones',
        'description': 'High-quality wireless headphones with noise cancellation',
        'price': Decimal('99.99'),
        'category': 'electronics',
        'stock': 50,
        'image_url': 'https://example.com/headphones.jpg'
    },
    {
        'product_id': 'prod-002', 
        'name': 'Smart Watch',
        'description': 'Feature-rich smartwatch with health tracking',
        'price': Decimal('199.99'),
        'category': 'electronics',
        'stock': 30,
        'image_url': 'https://example.com/smartwatch.jpg'
    },
    {
        'product_id': 'prod-003',
        'name': 'Coffee Mug',
        'description': 'Ceramic coffee mug with custom design',
        'price': Decimal('12.99'),
        'category': 'home',
        'stock': 100,
        'image_url': 'https://example.com/mug.jpg'
    }
]

for product in sample_products:
    table.put_item(Item=product)
    print(f'Added product: {product[\"name\"]}')

print('✅ Sample data seeded successfully')
"
    
    echo -e "${GREEN}✅ Sample data seeded${NC}"
}

# Main deployment flow
main() {
    echo -e "${GREEN}🛒 Serverless E-Commerce Platform Deployment${NC}"
    echo "=============================================="
    
    check_prerequisites
    package_lambdas
    deploy_infrastructure
    seed_data
    
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set up API Gateway endpoints"
    echo "2. Deploy frontend application"
    echo "3. Configure custom domain (optional)"
    echo ""
    echo "Check AWS Console for deployed resources."
}

# Run main function
main "$@"