# 🚀 Quick Start - Deploy to AWS

## Prerequisites
- AWS Account (free tier eligible)
- AWS CLI installed
- Terraform installed

## 1-Minute Setup

### Step 1: Configure AWS
```bash
./aws-setup.sh
```

### Step 2: Deploy Everything
```bash
./deploy-aws.sh
```

### Step 3: Access Your Site
Your e-commerce site will be live at the CloudFront URL provided!

## What Gets Deployed

### ✅ Frontend (React)
- **S3 Bucket** - Static website hosting
- **CloudFront** - Global CDN distribution
- **Custom Domain** - Optional (configure manually)

### ✅ Backend (Serverless)
- **Lambda Functions** - Products & Cart APIs
- **API Gateway** - REST API endpoints
- **DynamoDB** - NoSQL database tables

### ✅ Security & Auth
- **Cognito** - User authentication
- **IAM Roles** - Secure permissions
- **HTTPS** - SSL/TLS encryption

### ✅ Monitoring
- **CloudWatch** - Logs and metrics
- **X-Ray** - Distributed tracing (optional)

## Cost Estimate
- **Free Tier**: $0-5/month for low traffic
- **Production**: $10-50/month depending on usage

## Architecture
```
Internet → CloudFront → S3 (Frontend)
Internet → API Gateway → Lambda → DynamoDB
```

## Cleanup
```bash
cd infrastructure
terraform destroy
```

## Troubleshooting

### Common Issues:
1. **AWS Credentials**: Run `aws configure`
2. **Terraform State**: Delete `.terraform` folder and re-run
3. **Lambda Timeout**: Increase timeout in `main.tf`

### Support:
- Check CloudWatch logs for errors
- Verify IAM permissions
- Test API endpoints individually

---

🎉 **You now have a production-ready serverless e-commerce platform on AWS!**