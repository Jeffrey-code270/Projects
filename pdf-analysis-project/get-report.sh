#!/bin/bash
# Quick report access script

echo "📊 PDF Processing Pipeline Reports"
echo "=================================="
echo ""
echo "Choose report type:"
echo "1) Console Dashboard (immediate)"
echo "2) JSON Report (for automation)"
echo "3) Start Web Dashboard (browser access)"
echo "4) Send Email Report"
echo "5) Send Slack Report"
echo "6) View Log Files"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo "🖥️ Console Dashboard:"
        python3 pdf-analysis-project/app/dashboard.py
        ;;
    2)
        echo "📄 JSON Report:"
        python3 -c "
from pdf-analysis-project.app.dashboard import MonitoringDashboard
import json
monitor = MonitoringDashboard()
print(json.dumps(monitor.generate_report(), indent=2, default=str))
"
        ;;
    3)
        echo "🌐 Starting web dashboard at http://localhost:8080"
        echo "Press Ctrl+C to stop"
        cd pdf-analysis-project && python3 app/web_dashboard.py
        ;;
    4)
        echo "📧 Sending email report..."
        python3 pdf-analysis-project/app/email_reports.py
        ;;
    5)
        echo "💬 Sending Slack report..."
        python3 pdf-analysis-project/app/slack_reports.py
        ;;
    6)
        echo "📋 Recent Log Files:"
        echo ""
        echo "=== Application Logs ==="
        tail -20 pdf-analysis-project/logs/app.log 2>/dev/null || echo "No app logs found"
        echo ""
        echo "=== Alert Logs ==="
        tail -10 pdf-analysis-project/logs/alerts.log 2>/dev/null || echo "No alerts found"
        echo ""
        echo "=== Metrics ==="
        cat pdf-analysis-project/logs/metrics.json 2>/dev/null || echo "No metrics found"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac