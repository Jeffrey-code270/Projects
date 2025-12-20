#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from dashboard import MonitoringDashboard

class SlackReporter:
    def __init__(self):
        # Set this in your .env file
        self.webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    
    def send_report(self):
        """Send monitoring report to Slack."""
        monitor = MonitoringDashboard()
        data = monitor.generate_report()
        
        # Create Slack message
        message = {
            "text": "📊 PDF Processing Pipeline Report",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📊 PDF Processing Pipeline Report"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Generated:* {data['timestamp']}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🖥️ System Status*\\n• CPU: {data['system']['cpu_usage']:.1f}%\\n• Memory: {data['system']['memory_usage']:.1f}%\\n• Disk: {data['system']['disk_usage']:.1f}%"
                    }
                }
            ]
        }
        
        # Add database status
        if data['database'].get('database_status') == 'healthy':
            db_text = f"*🗄️ Database Status*\\n✅ Healthy\\n• Keywords: {data['database']['total_keywords']}\\n• PDFs: {data['database']['unique_pdfs']}"
        else:
            db_text = f"*🗄️ Database Status*\\n❌ Error: {data['database'].get('error', 'Unknown')}"
        
        message["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": db_text
            }
        })
        
        try:
            response = requests.post(self.webhook_url, json=message)
            if response.status_code == 200:
                print("✅ Report sent to Slack")
                return True
            else:
                print(f"❌ Failed to send to Slack: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Slack error: {e}")
            return False

if __name__ == "__main__":
    reporter = SlackReporter()
    reporter.send_report()