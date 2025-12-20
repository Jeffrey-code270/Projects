#!/bin/bash
# Setup automated monitoring with cron jobs

echo "Setting up automated monitoring..."

# Make monitoring script executable
chmod +x /home/ubuntu/pdf-analysis-project/deployment/monitor.sh

# Add cron jobs for monitoring
(crontab -l 2>/dev/null; echo "# PDF Processing Pipeline Monitoring") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/ubuntu/pdf-analysis-project/deployment/monitor.sh >> /var/log/pdf-monitor.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 */6 * * * /home/ubuntu/pdf-analysis-project/deployment/cleanup-logs.sh") | crontab -

echo "✅ Monitoring cron jobs added:"
echo "   - Health checks every 5 minutes"
echo "   - Log cleanup every 6 hours"

# Create log cleanup script
cat > /home/ubuntu/pdf-analysis-project/deployment/cleanup-logs.sh << 'EOF'
#!/bin/bash
# Clean up old log files

LOG_DIR="/app/logs"
find $LOG_DIR -name "*.log" -mtime +7 -delete
find $LOG_DIR -name "*.json" -mtime +3 -delete
echo "$(date): Log cleanup completed" >> /var/log/pdf-monitor.log
EOF

chmod +x /home/ubuntu/pdf-analysis-project/deployment/cleanup-logs.sh

echo "✅ Monitoring setup complete!"