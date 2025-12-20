#!/bin/bash
# AWS Setup Helper Script

echo "🔧 AWS Setup Helper for Serverless E-Commerce"
echo "=============================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Installing..."
    
    # Install AWS CLI based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
        sudo installer -pkg AWSCLIV2.pkg -target /
        rm AWSCLIV2.pkg
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        rm -rf aws awscliv2.zip
    fi
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Please install from: https://terraform.io/downloads"
    exit 1
fi

# Configure AWS credentials
echo "🔑 Configuring AWS credentials..."
echo "You'll need:"
echo "  - AWS Access Key ID"
echo "  - AWS Secret Access Key"
echo "  - Default region (e.g., us-east-1)"
echo ""

aws configure

# Verify configuration
echo "🔍 Verifying AWS configuration..."
if aws sts get-caller-identity; then
    echo "✅ AWS configuration successful!"
    
    # Show account info
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    REGION=$(aws configure get region)
    
    echo ""
    echo "📋 Your AWS Configuration:"
    echo "   Account ID: $ACCOUNT_ID"
    echo "   Region: $REGION"
    echo ""
    echo "🚀 Ready to deploy! Run: ./deploy-aws.sh"
else
    echo "❌ AWS configuration failed. Please check your credentials."
    exit 1
fi