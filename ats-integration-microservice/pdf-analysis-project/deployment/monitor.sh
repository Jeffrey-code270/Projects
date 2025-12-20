#!/bin/bash
# Monitoring script for PDF processing pipeline

LOG_DIR="/app/logs"
ALERT_LOG="$LOG_DIR/alerts.log"

# Create logs directory if it doesn't exist
mkdir -p $LOG_DIR

echo "=== PDF Processing Pipeline Monitor ==="
echo "Started at: $(date)"

# Function to check Docker containers
check_containers() {
    echo "🐳 Checking Docker containers..."
    docker-compose ps
    
    # Check if all containers are running
    if ! docker-compose ps | grep -q "Up"; then
        echo "❌ Some containers are not running!"
        return 1
    fi
    echo "✅ All containers are running"
    return 0
}

# Function to check disk space
check_disk_space() {
    echo "💾 Checking disk space..."
    df -h /
    
    DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $DISK_USAGE -gt 90 ]; then
        echo "❌ Disk usage is high: ${DISK_USAGE}%"
        return 1
    fi
    echo "✅ Disk usage is normal: ${DISK_USAGE}%"
    return 0
}

# Function to check database connectivity
check_database() {
    echo "🗄️ Checking database connectivity..."
    if docker-compose exec -T postgres pg_isready -U postgres; then
        echo "✅ Database is accessible"
        return 0
    else
        echo "❌ Database connection failed"
        return 1
    fi
}

# Function to check application health
check_application() {
    echo "📱 Checking application health..."
    if docker-compose exec -T app python app/health_check.py; then
        echo "✅ Application health check passed"
        return 0
    else
        echo "❌ Application health check failed"
        return 1
    fi
}

# Function to show recent logs
show_recent_logs() {
    echo "📋 Recent application logs:"
    if [ -f "$LOG_DIR/app.log" ]; then
        tail -10 "$LOG_DIR/app.log"
    else
        echo "No application logs found"
    fi
}

# Function to show alerts
show_alerts() {
    echo "🚨 Recent alerts:"
    if [ -f "$ALERT_LOG" ]; then
        tail -5 "$ALERT_LOG"
    else
        echo "No alerts found"
    fi
}

# Main monitoring loop
main() {
    local exit_code=0
    
    check_containers || exit_code=1
    echo ""
    
    check_disk_space || exit_code=1
    echo ""
    
    check_database || exit_code=1
    echo ""
    
    check_application || exit_code=1
    echo ""
    
    show_recent_logs
    echo ""
    
    show_alerts
    echo ""
    
    # Run Python dashboard
    echo "📊 System Dashboard:"
    docker-compose exec -T app python app/dashboard.py
    
    # Run alert checks
    echo "🔍 Running health checks..."
    docker-compose exec -T app python app/alerts.py
    
    echo "Monitor completed at: $(date)"
    return $exit_code
}

# Run monitoring
main