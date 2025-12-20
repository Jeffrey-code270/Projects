#!/usr/bin/env python3
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dashboard import MonitoringDashboard

class EmailReporter:
    def __init__(self):
        # Configure these in your .env file
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = "your-email@gmail.com"  # Set in .env
        self.email_password = "your-app-password"  # Set in .env
        self.recipient = "admin@yourcompany.com"  # Set in .env
    
    def generate_email_report(self):
        """Generate HTML email report."""
        monitor = MonitoringDashboard()
        data = monitor.generate_report()
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>📊 PDF Processing Pipeline Report</h2>
            <p><strong>Generated:</strong> {data['timestamp']}</p>
            
            <h3>🖥️ System Status</h3>
            <ul>
                <li>CPU Usage: {data['system']['cpu_usage']:.1f}%</li>
                <li>Memory Usage: {data['system']['memory_usage']:.1f}%</li>
                <li>Disk Usage: {data['system']['disk_usage']:.1f}%</li>
                <li>Uptime: {data['system']['uptime']}</li>
            </ul>
            
            <h3>🗄️ Database Status</h3>
        """
        
        if data['database'].get('database_status') == 'healthy':
            html_content += f"""
            <p style="color: green;">✅ Database is healthy</p>
            <ul>
                <li>Total Keywords: {data['database']['total_keywords']}</li>
                <li>Unique PDFs: {data['database']['unique_pdfs']}</li>
                <li>Recent Activity (24h): {data['database']['recent_activity_24h']}</li>
            </ul>
            """
        else:
            html_content += f"""
            <p style="color: red;">❌ Database Error: {data['database'].get('error', 'Unknown')}</p>
            """
        
        html_content += """
            <h3>📱 Application Metrics</h3>
        """
        
        if 'pdfs_processed' in data['application']:
            html_content += f"""
            <ul>
                <li>PDFs Processed: {data['application']['pdfs_processed']}</li>
                <li>Keywords Found: {data['application']['total_keywords']}</li>
                <li>Average Process Time: {data['application']['avg_processing_time']:.2f}s</li>
                <li>Error Count: {data['application']['error_count']}</li>
            </ul>
            """
        else:
            html_content += "<p>No recent processing activity</p>"
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    def send_report(self):
        """Send email report."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"PDF Pipeline Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            msg['From'] = self.email_user
            msg['To'] = self.recipient
            
            html_part = MIMEText(self.generate_email_report(), 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Report sent to {self.recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

if __name__ == "__main__":
    reporter = EmailReporter()
    reporter.send_report()