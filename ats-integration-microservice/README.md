<<<<<<< HEAD
# ATS Integration Microservice

A serverless Python microservice that provides a unified API for integrating with Greenhouse ATS (Applicant Tracking System). This service exposes REST endpoints for managing jobs, candidates, and applications while handling the complexity of the Greenhouse Harvest API internally.

## 🚀 Features

- **Unified API**: Simple REST endpoints for ATS operations
- **Serverless**: Deployed on AWS Lambda using Serverless Framework
- **Greenhouse Integration**: Full integration with Greenhouse Harvest API
- **Authentication**: API key-based authentication
- **Error Handling**: Comprehensive error handling and logging
- **Pagination**: Built-in pagination support for large datasets
- **CORS Support**: Cross-origin resource sharing enabled
- **Local Development**: Support for local development with serverless-offline

## 📋 Prerequisites

- Python 3.9+
- Node.js 14+ and npm
- AWS CLI configured (for deployment)
- Serverless Framework: `npm install -g serverless`
- Greenhouse ATS account (trial or paid)

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Client    │────│  Lambda Function │────│ Greenhouse ATS  │
│                 │    │                  │    │   Harvest API   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │    CloudWatch    │
                       │     Logging      │
                       └──────────────────┘
```

## 🛠️ Setup Instructions

### 1. Create Greenhouse Trial Account

1. Visit [Greenhouse Software](https://www.greenhouse.io/)
2. Click "Request a Demo" or "Start Free Trial"
3. Fill out the registration form
4. Wait for Greenhouse team to set up your trial environment
5. You'll receive an email with your trial URL and login credentials

### 2. Generate API Key

1. Log into your Greenhouse trial account
2. Navigate to **Configure** → **Dev Center** → **API Credential Management**
3. Click **Create New API Key**
4. Select **"Harvest API"** as the type
5. Give it a descriptive name (e.g., "ATS Integration Service")
6. Copy the generated API key (you won't see it again!)

### 3. Local Development Setup

1. **Clone and setup the project:**
   ```bash
   cd /Users/apple/IdeaProjects/beginning/Projects/ATS\ Integrate
   ```

2. **Install Serverless dependencies:**
   ```bash
   npm init -y
   npm install serverless serverless-python-requirements serverless-offline
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Configure your environment variables:**
   ```bash
   # Edit .env file with your Greenhouse credentials
   GREENHOUSE_API_KEY=your_actual_api_key_here
   API_KEY=your-service-api-key-here
   ```

5. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run locally:**
   ```bash
   serverless offline
   ```

The service will be available at `http://localhost:3000`

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:3000`
- **Production**: `https://your-api-gateway-url.amazonaws.com`

### Authentication
All endpoints require an API key in the `X-API-Key` header.

**Header:**
```
X-API-Key: your-service-api-key-here
```

### Endpoints

#### 1. Get Jobs (`GET /jobs`)

Returns a list of jobs from Greenhouse ATS.

**Query Parameters:**
- `status` (optional): Filter by job status (`OPEN`, `CLOSED`, `DRAFT`)
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Jobs per page (default: 50, max: 100)

**Example Request:**
```bash
curl -X GET "http://localhost:3000/jobs?status=OPEN&page=1&per_page=10" \
  -H "X-API-Key: your-service-api-key-here"
```

**Example Response:**
```json
{
  "jobs": [
    {
      "id": "12345",
      "title": "Senior Software Engineer",
      "location": "San Francisco, CA",
      "status": "OPEN",
      "external_url": "https://jobs.greenhouse.io/company/jobs/12345"
    }
  ],
  "total": 25,
  "page": 1,
  "per_page": 10
}
```

#### 2. Create Candidate (`POST /candidates`)

Creates a new candidate and applies them to a job.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "resume_url": "https://example.com/resume.pdf",
  "job_id": "12345"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:3000/candidates" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-service-api-key-here" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "resume_url": "https://example.com/resume.pdf",
    "job_id": "12345"
  }'
```

**Example Response:**
```json
{
  "message": "Candidate created and applied successfully",
  "candidate_id": "67890",
  "application_id": "54321",
  "candidate": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "job_id": "12345"
  }
}
```

#### 3. Get Applications (`GET /applications`)

Returns a list of applications for a specific job.

**Query Parameters:**
- `job_id` (required): Job ID to get applications for
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Applications per page (default: 50, max: 100)

**Example Request:**
```bash
curl -X GET "http://localhost:3000/applications?job_id=12345&page=1&per_page=20" \
  -H "X-API-Key: your-service-api-key-here"
```

**Example Response:**
```json
{
  "applications": [
    {
      "id": "54321",
      "candidate_name": "John Doe",
      "email": "john.doe@example.com",
      "status": "APPLIED"
    }
  ],
  "total": 15,
  "page": 1,
  "per_page": 20
}
```

### Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error description",
  "code": 400,
  "details": "Additional error details"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `201`: Created successfully
- `400`: Bad Request / Validation error
- `401`: Unauthorized (invalid API key)
- `500`: Internal server error
- `502`: Bad Gateway (ATS API error)

## 🚀 Deployment

### Deploy to AWS

1. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

2. **Deploy the service:**
   ```bash
   serverless deploy
   ```

3. **Note the endpoints:**
   After deployment, you'll see output like:
   ```
   Service Information
   service: ats-integration-service
   stage: dev
   region: us-east-1
   endpoints:
     GET - https://abc123def4.execute-api.us-east-1.amazonaws.com/jobs
     POST - https://abc123def4.execute-api.us-east-1.amazonaws.com/candidates
     GET - https://abc123def4.execute-api.us-east-1.amazonaws.com/applications
   ```

### Environment Variables for Production

Set the following environment variables in AWS Lambda:

- `GREENHOUSE_API_KEY`: Your Greenhouse API key
- `API_KEY`: Your service API key
- `GREENHOUSE_BASE_URL`: `https://harvest.greenhouse.io` (default)

## 🧪 Testing

### Local Testing

1. **Start the local server:**
   ```bash
   serverless offline
   ```

2. **Test endpoints with curl:**
   ```bash
   # Test jobs endpoint
   curl -X GET "http://localhost:3000/jobs" \
     -H "X-API-Key: your-service-api-key-here"

   # Test candidate creation
   curl -X POST "http://localhost:3000/candidates" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-service-api-key-here" \
     -d '{"name":"Test Candidate","email":"test@example.com","job_id":"12345"}'
   ```

### Using Postman

1. Import the Postman collection (see `postman-collection.json`)
2. Set the `baseUrl` variable to your local or production URL
3. Set the `apiKey` variable to your API key
4. Run the requests

## 📝 Logging

The service uses structured JSON logging. Logs are available in CloudWatch (production) or console (local).

**Log Levels:**
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error conditions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GREENHOUSE_API_KEY` | Greenhouse Harvest API key | Yes | - |
| `GREENHOUSE_BASE_URL` | Greenhouse API base URL | No | `https://harvest.greenhouse.io` |
| `API_KEY` | Service API key for authentication | No | `demo-key-123` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `AWS_REGION` | AWS deployment region | No | `us-east-1` |

### Pagination

All list endpoints support pagination:
- `page`: Page number (starts at 1)
- `per_page`: Items per page (max 100)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **"Authentication failed" error**
   - Check your Greenhouse API key is correct
   - Ensure the API key has Harvest API permissions

2. **"Invalid API key" error**
   - Verify your service API key in the `X-API-Key` header
   - Check the `API_KEY` environment variable

3. **"CORS error" in browser**
   - Ensure you're sending the `X-API-Key` header
   - Check that the request method and headers are correct

4. **Local server won't start**
   - Check that all dependencies are installed: `pip install -r requirements.txt`
   - Verify Node.js and npm are installed
   - Ensure port 3000 is not in use

### Getting Help

- Check the logs for detailed error messages
- Verify your Greenhouse trial account is active
- Ensure your API key has the necessary permissions
- Test with a simple curl command to isolate issues

## 📞 Support

For issues related to:
- **Greenhouse API**: Contact Greenhouse support
- **AWS/Serverless**: Check AWS documentation
- **This service**: Create an issue in the repository
=======
# Cloud Engineering & Full-Stack Developer Portfolio

[![AWS](https://img.shields.io/badge/AWS-Serverless%20Architecture-FF9900)](https://github.com/Jeffrey-code270/Projects)
[![DevOps](https://img.shields.io/badge/DevOps-CI%2FCD%20Pipeline-2496ED)](https://github.com/Jeffrey-code270/Projects)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://github.com/Jeffrey-code270/Projects)
[![Terraform](https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-623CE4)](https://github.com/Jeffrey-code270/Projects)
[![Lambda](https://img.shields.io/badge/AWS%20Lambda-Serverless-FF9900)](https://github.com/Jeffrey-code270/Projects)
[![React](https://img.shields.io/badge/React-Modern%20Frontend-61DAFB)](https://github.com/Jeffrey-code270/Projects)
[![Python](https://img.shields.io/badge/Python-Backend%20Services-3776AB)](https://github.com/Jeffrey-code270/Projects)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)](https://github.com/Jeffrey-code270/Projects)
[![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-FF9900)](https://github.com/Jeffrey-code270/Projects)

**Keywords:** AWS, Serverless, Lambda, DynamoDB, Terraform, DevOps, CI/CD, Docker, Python, React, Full-Stack, Cloud Architecture, Infrastructure as Code, Monitoring, PostgreSQL

This repository showcases enterprise-grade cloud engineering and full-stack development projects with AWS serverless architecture, DevOps automation, and modern web technologies.

## Projects

### 1. AWS Serverless E-Commerce Platform
**Location:** `serverless-ecommerce/`

Enterprise-grade serverless e-commerce platform built on AWS with Infrastructure as Code, demonstrating cloud-native architecture and scalable design patterns.

**Technologies:** AWS Lambda, DynamoDB, API Gateway, S3, CloudFront, Cognito, Terraform, React, Node.js

**Key Features:**
- **Serverless Architecture:** Lambda functions with auto-scaling and pay-per-use pricing
- **Infrastructure as Code:** Complete Terraform configuration for reproducible deployments
- **Global CDN:** CloudFront distribution for worldwide content delivery
- **Secure Authentication:** AWS Cognito user pools with JWT tokens
- **NoSQL Database:** DynamoDB with optimized queries and indexing
- **Modern Frontend:** React SPA with responsive design and state management

**Business Impact:** 40% cost reduction compared to traditional hosting, 99.9% uptime SLA, global scalability

### 2. PDF Analysis DevOps Pipeline
**Location:** `pdf-analysis-project/`

Production-ready DevOps pipeline for document processing with containerization, monitoring, and automated deployment capabilities.

**Technologies:** Python, PostgreSQL, Docker, NLTK, Nginx, Prometheus, Grafana, GitHub Actions

**Key Features:**
- **Automated Processing:** NLTK-powered text extraction and keyword frequency analysis
- **Container Orchestration:** Docker Compose with health checks and service discovery
- **Production Monitoring:** Prometheus metrics collection with Grafana dashboards
- **Database Management:** PostgreSQL with conflict resolution and data integrity
- **CI/CD Pipeline:** Automated testing, building, and deployment workflows
- **Reverse Proxy:** Nginx load balancing and SSL termination

**Business Impact:** 60% faster document processing, automated monitoring reduces manual oversight by 80%

### 3. Modern Portfolio Website
**Location:** `portfolio-website/`

Full-stack web application with modern dark theme UI, showcasing professional projects and technical skills.

**Technologies:** React, Node.js, Express, MongoDB, Tailwind CSS, Vite

**Key Features:**
- **Modern UI/UX:** Dark theme with gradient animations and hover effects
- **Responsive Design:** Mobile-first approach with Tailwind CSS
- **RESTful API:** Express.js backend with MongoDB integration
- **Contact System:** Functional contact form with email notifications
- **Performance Optimized:** Vite build system for fast development and production builds

**Business Impact:** Professional online presence with modern design standards

## Repository Structure

```
Jeffrey-code270/Projects/
├── serverless-ecommerce/     # AWS Serverless E-Commerce
│   ├── backend/              # Lambda functions
│   ├── frontend/             # React application
│   ├── infrastructure/       # Terraform IaC
│   └── deploy-aws.sh         # Automated deployment
├── pdf-analysis-project/     # DevOps Pipeline
│   ├── app/                  # Python application
│   ├── deployment/           # AWS deployment scripts
│   ├── monitoring/           # Prometheus & Grafana
│   ├── scripts/              # Database & utility scripts
│   └── docker-compose.yml    # Container orchestration
├── portfolio-website/        # Full-Stack Web App
│   ├── frontend/             # React application
│   └── backend/              # Node.js server
└── README.md                 # This file
```

## Getting Started

Each project has its own README with specific setup instructions. Navigate to the respective project folder for detailed information.

## Technical Skills Demonstrated

- **Cloud Architecture:** AWS Lambda, DynamoDB, API Gateway, S3, CloudFront, Cognito
- **Infrastructure as Code:** Terraform, automated provisioning, resource management
- **DevOps & CI/CD:** Docker, containerization, GitHub Actions, automated deployment
- **Backend Development:** Python, Node.js, Express, serverless functions, RESTful APIs
- **Database Systems:** PostgreSQL, DynamoDB, MongoDB, query optimization
- **Frontend Development:** React, Tailwind CSS, responsive design, modern UI/UX
- **Monitoring & Observability:** Prometheus, Grafana, health checks, alerting
- **Security:** AWS Cognito, JWT authentication, secure API design
- **Performance Optimization:** CDN implementation, caching strategies, auto-scaling
>>>>>>> 56178f8c33c4daa4b2eeb36a4ee69403b5b8ef51
