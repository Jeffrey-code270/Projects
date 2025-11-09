# Automated Document Processing Pipeline

Built an automated document processing pipeline that extracts and cleans text from PDFs, analyzes keyword frequency, and stores results in a PostgreSQL database. Containerized with Docker, integrated with GitHub for version control, and deployed to AWS EC2 via a CI/CD pipeline using GitHub Actions. Configured and monitored the Linux server to ensure continuous availability.

## 🚀 Features

- **Automated PDF Processing**: Extract and clean text from PDF documents
- **Keyword Analysis**: Frequency analysis with NLTK
- **Database Storage**: PostgreSQL with conflict resolution
- **Containerization**: Docker and Docker Compose
- **CI/CD Pipeline**: GitHub Actions for automated deployment
- **AWS Deployment**: EC2 with monitoring and health checks
- **Production Ready**: Nginx reverse proxy, SSL support

## 🛠 Technologies

- **Backend**: Python, PostgreSQL, NLTK
- **DevOps**: Docker, GitHub Actions, AWS EC2
- **Infrastructure**: Nginx, Linux server management
- **Monitoring**: Health checks, logging, system monitoring

## 📋 Setup

### Local Development
```bash
# Clone repository
git clone https://github.com/Jeffrey-code270/Projects.git
cd Projects/pdf-analysis-project

# Install dependencies
pip install -r requirements.txt
python setup.py

# Start services
docker-compose up -d

# Run pipeline
python app/process_pdfs.py
```

### AWS EC2 Deployment
```bash
# Run setup script on EC2 instance
bash deployment/ec2-setup.sh

# Configure environment
cp .env.example .env
# Edit .env with production values

# Deploy with CI/CD
git push origin main  # Triggers GitHub Actions
```

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│ GitHub Actions│───▶│   AWS EC2      │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                     │
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│     Nginx       │◀───│    Docker    │◀───│  Python App    │
│  (Reverse Proxy)│    │  Containers  │    │ (PDF Processing)│
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                     │
                       ┌──────────────┐    ┌─────────────────┐
                       │ Health Checks│    │   PostgreSQL   │
                       │ & Monitoring │    │   Database     │
                       └──────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
pdf-analysis-project/
├── .github/workflows/     # CI/CD pipeline
├── app/                   # Application code
│   ├── process_pdfs.py   # Main processing script
│   └── health_check.py   # System monitoring
├── deployment/            # AWS deployment scripts
├── data/                  # PDF files
├── scripts/              # Database scripts
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # Application container
└── README.md             # Documentation
```

## 🔧 CI/CD Pipeline

1. **Code Push** → GitHub repository
2. **Automated Testing** → GitHub Actions
3. **Build & Deploy** → AWS EC2 instance
4. **Health Monitoring** → Continuous availability

## 📊 Monitoring

- Health check endpoints
- Database connectivity monitoring
- Disk space monitoring
- Application logs
- System resource monitoring