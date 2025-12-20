#!/bin/bash
# Simple report script

echo "📊 PDF Processing Report"
cd "$(dirname "$0")"
python3 -c "
import sqlite3
from datetime import datetime

conn = sqlite3.connect('pdf_analysis.db')
cursor = conn.cursor()

print('\n🗄️ DATABASE STATUS')
cursor.execute('SELECT COUNT(*) FROM keyword_frequency')
total = cursor.fetchone()[0]
print(f'   Total Keywords: {total}')

cursor.execute('SELECT COUNT(DISTINCT pdf_name) FROM keyword_frequency')
pdfs = cursor.fetchone()[0]
print(f'   PDFs Processed: {pdfs}')

print('\n📊 TOP KEYWORDS')
cursor.execute('SELECT pdf_name, keyword, frequency FROM keyword_frequency ORDER BY frequency DESC LIMIT 5')
for pdf, keyword, freq in cursor.fetchall():
    print(f'   {pdf}: {keyword} ({freq}x)')

print(f'\n⏰ {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}\n')
conn.close()
"