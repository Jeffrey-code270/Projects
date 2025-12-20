#!/usr/bin/env python3
import smtplib
import psutil
import json
import os
from email.mime.text import MIMEText
from datetime import datetime
from monitoring import logger

class AlertManager:
    def __init__(self):
        self.thresholds = {
            'cpu_threshold': 80,
            'memory_threshold': 85,
            'disk_threshold': 90,
            'error_threshold': 5
        }
        
    def check_system_health(self):
        """Check system health and trigger alerts if needed."""
        alerts = []
        
        # CPU check
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > self.thresholds['cpu_threshold']:
            alerts.append(f"🚨 HIGH CPU USAGE: {cpu_usage:.1f}%")
        
        # Memory check
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > self.thresholds['memory_threshold']:
            alerts.append(f"🚨 HIGH MEMORY USAGE: {memory_usage:.1f}%")
        
        # Disk check
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage > self.thresholds['disk_threshold']:
            alerts.append(f"🚨 HIGH DISK USAGE: {disk_usage:.1f}%")
        
        return alerts
    
    def check_application_health(self):
        """Check application-specific health metrics."""
        alerts = []
        
        try:
            with open('/app/logs/metrics.json', 'r') as f:
                metrics = json.load(f)
            
            # Check error rate
            if metrics.get('error_count', 0) > self.thresholds['error_threshold']:
                alerts.append(f"🚨 HIGH ERROR COUNT: {metrics['error_count']} errors")
            
            # Check if processing is taking too long
            avg_time = metrics.get('avg_processing_time', 0)
            if avg_time > 30:  # 30 seconds threshold
                alerts.append(f"⚠️ SLOW PROCESSING: {avg_time:.1f}s average")
                
        except FileNotFoundError:
            alerts.append("⚠️ No application metrics available")
        
        return alerts
    
    def send_alert(self, message):
        """Log alert (extend this to send emails/Slack notifications)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] ALERT: {message}"
        
        # Log to file
        logger.warning(alert_msg)
        
        # Write to alerts file
        with open('/app/logs/alerts.log', 'a') as f:
            f.write(alert_msg + "\\n")
        
        print(alert_msg)
    
    def run_health_check(self):
        """Run complete health check and send alerts."""
        all_alerts = []
        all_alerts.extend(self.check_system_health())
        all_alerts.extend(self.check_application_health())
        
        if all_alerts:
            for alert in all_alerts:
                self.send_alert(alert)
        else:
            logger.info("✅ All systems healthy")
        
        return len(all_alerts) == 0

if __name__ == "__main__":
    alert_manager = AlertManager()
    alert_manager.run_health_check()