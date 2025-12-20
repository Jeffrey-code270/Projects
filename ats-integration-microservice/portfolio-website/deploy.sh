#!/bin/bash

echo "🚀 Deploying Portfolio Website..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building project..."
npm run build

echo "✅ Build complete! Ready for deployment."
echo "📁 Built files are in: frontend/dist/"
echo ""
echo "🌐 Deploy options:"
echo "1. Netlify: Connect your GitHub repo to Netlify for automatic deployments"
echo "2. Vercel: Import your GitHub repo to Vercel"
echo "3. GitHub Pages: Enable GitHub Pages in repository settings"
echo ""
echo "🔗 Your site will be available at: https://your-username.netlify.app"