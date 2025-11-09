#!/usr/bin/env python3
import json
import os
import psutil
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class MonitoringDashboard:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD")
        }
    
    def get_system_status(self):
        """Get current system metrics."""
        return {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime': datetime.now() - datetime.fromtimestamp(psutil.boot_time()),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_database_stats(self):
        """Get database statistics."""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM keyword_frequency")
            total_records = cursor.fetchone()[0]
            
            # Unique PDFs processed
            cursor.execute("SELECT COUNT(DISTINCT pdf_name) FROM keyword_frequency")
            unique_pdfs = cursor.fetchone()[0]
            
            # Recent activity (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM keyword_frequency 
                WHERE created_at > NOW() - INTERVAL '24 hours'
            """)
            recent_activity = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_keywords': total_records,
                'unique_pdfs': unique_pdfs,
                'recent_activity_24h': recent_activity,
                'database_status': 'healthy'
            }
        except Exception as e:
            return {
                'database_status': 'error',
                'error': str(e)
            }
    
    def get_application_metrics(self):
        """Read application metrics from log file."""
        try:
            with open('/app/logs/metrics.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'status': 'No metrics available'}
    
    def generate_report(self):
        """Generate comprehensive monitoring report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system': self.get_system_status(),
            'database': self.get_database_stats(),
            'application': self.get_application_metrics()
        }
        
        # Save report
        with open('/app/logs/monitoring_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report
    
    def print_dashboard(self):
        """Print formatted dashboard to console."""
        report = self.generate_report()
        
        print("\\n" + "="*60)
        print("           PDF PROCESSING PIPELINE DASHBOARD")
        print("="*60)
        
        # System Status
        system = report['system']
        print(f"\\n🖥️  SYSTEM STATUS")
        print(f"   CPU Usage:    {system['cpu_usage']:.1f}%")
        print(f"   Memory Usage: {system['memory_usage']:.1f}%")
        print(f"   Disk Usage:   {system['disk_usage']:.1f}%")
        print(f"   Uptime:       {system['uptime']}")
        
        # Database Status
        db = report['database']
        print(f"\\n🗄️  DATABASE STATUS")
        if db.get('database_status') == 'healthy':
            print(f"   Status:       ✅ Healthy")
            print(f"   Total Keywords: {db['total_keywords']}")
            print(f"   Unique PDFs:    {db['unique_pdfs']}")
            print(f"   Recent Activity: {db['recent_activity_24h']} (24h)")
        else:
            print(f"   Status:       ❌ Error - {db.get('error', 'Unknown')}")
        
        # Application Metrics
        app = report['application']
        print(f"\\n📊 APPLICATION METRICS")
        if 'pdfs_processed' in app:
            print(f"   PDFs Processed: {app['pdfs_processed']}")
            print(f"   Keywords Found: {app['total_keywords']}")
            print(f"   Avg Process Time: {app['avg_processing_time']:.2f}s")
            print(f"   Error Count:    {app['error_count']}")
        else:
            print(f"   Status:       No recent activity")
        
        print(f"\\n⏰ Last Updated: {report['timestamp']}")
        print("="*60 + "\\n")

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    dashboard.print_dashboard()