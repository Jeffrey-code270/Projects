#!/usr/bin/env python3
from flask import Flask, jsonify, render_template_string
import json
import os
from dashboard import MonitoringDashboard

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PDF Processing Pipeline Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .status-ok { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
        .header { text-align: center; color: #333; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">📊 PDF Processing Pipeline Dashboard</h1>
        <p class="header">Last Updated: {{ data.timestamp }}</p>
        
        <div class="grid">
            <div class="card">
                <h2>🖥️ System Status</h2>
                <div class="metric">CPU: <strong>{{ "%.1f"|format(data.system.cpu_usage) }}%</strong></div>
                <div class="metric">Memory: <strong>{{ "%.1f"|format(data.system.memory_usage) }}%</strong></div>
                <div class="metric">Disk: <strong>{{ "%.1f"|format(data.system.disk_usage) }}%</strong></div>
                <div class="metric">Uptime: <strong>{{ data.system.uptime }}</strong></div>
            </div>
            
            <div class="card">
                <h2>🗄️ Database Status</h2>
                {% if data.database.database_status == 'healthy' %}
                    <div class="status-ok">✅ Database Healthy</div>
                    <div class="metric">Total Keywords: <strong>{{ data.database.total_keywords }}</strong></div>
                    <div class="metric">Unique PDFs: <strong>{{ data.database.unique_pdfs }}</strong></div>
                    <div class="metric">Recent Activity: <strong>{{ data.database.recent_activity_24h }}</strong></div>
                {% else %}
                    <div class="status-error">❌ Database Error</div>
                    <div>{{ data.database.error }}</div>
                {% endif %}
            </div>
        </div>
        
        <div class="card">
            <h2>📱 Application Metrics</h2>
            {% if data.application.pdfs_processed %}
                <div class="metric">PDFs Processed: <strong>{{ data.application.pdfs_processed }}</strong></div>
                <div class="metric">Keywords Found: <strong>{{ data.application.total_keywords }}</strong></div>
                <div class="metric">Avg Process Time: <strong>{{ "%.2f"|format(data.application.avg_processing_time) }}s</strong></div>
                <div class="metric">Errors: <strong>{{ data.application.error_count }}</strong></div>
            {% else %}
                <div>No recent processing activity</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    monitor = MonitoringDashboard()
    data = monitor.generate_report()
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/api/status')
def api_status():
    monitor = MonitoringDashboard()
    return jsonify(monitor.generate_report())

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "pdf-processing-dashboard"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)