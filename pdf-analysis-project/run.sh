#!/bin/bash
# Simple run script for PDF processing project

echo "🚀 Starting PDF Processing Pipeline..."
cd "$(dirname "$0")"
python3 app/process_pdfs.py
echo "✅ Processing complete!"