#!/bin/bash
# EC2 Instance Setup Script

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Install monitoring tools
sudo apt install -y htop nginx certbot python3-certbot-nginx

# Clone repository
cd /home/ubuntu
git clone https://github.com/Jeffrey-code270/Projects.git
cd Projects/pdf-analysis-project

# Set up environment
cp .env.example .env
# Edit .env with production values

# Start services
docker-compose up -d

# Configure nginx reverse proxy
sudo tee /etc/nginx/sites-available/pdf-analysis > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/pdf-analysis /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo "EC2 setup complete!"