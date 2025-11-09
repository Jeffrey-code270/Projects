#!/bin/bash
# Simple web dashboard

echo "🌐 Starting web dashboard at http://localhost:8080"
cd "$(dirname "$0")"
python3 -c "
from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('pdf_analysis.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM keyword_frequency')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT pdf_name, keyword, frequency FROM keyword_frequency ORDER BY frequency DESC LIMIT 10')
    keywords = cursor.fetchall()
    
    html = '''
    <h1>📊 PDF Processing Dashboard</h1>
    <p><strong>Total Keywords:</strong> ''' + str(total) + '''</p>
    <h2>Top Keywords:</h2>
    <ul>'''
    
    for pdf, keyword, freq in keywords:
        html += f'<li><strong>{pdf}:</strong> {keyword} ({freq}x)</li>'
    
    html += '</ul><p><em>Auto-refresh every 30s</em></p>'
    html += '<meta http-equiv=\"refresh\" content=\"30\">'
    
    conn.close()
    return html

app.run(host='0.0.0.0', port=8080)
"