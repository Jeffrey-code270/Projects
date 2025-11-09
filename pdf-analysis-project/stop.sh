#!/bin/bash
# Simple stop script

echo "🛑 Stopping PDF Processing Project..."

# Kill Python processes
pkill -f "python3.*pdf" 2>/dev/null
pkill -f "python3.*flask" 2>/dev/null

# Kill processes on common ports
lsof -ti:8080 | xargs kill -9 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null

# Stop Docker if running
docker-compose down 2>/dev/null

echo "✅ Project stopped!"