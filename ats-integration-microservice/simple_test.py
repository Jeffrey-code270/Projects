#!/usr/bin/env python3

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.handlers.jobs import get_jobs
    print("✅ Import successful!")
    
    # Simple test
    event = {
        'httpMethod': 'GET',
        'headers': {'X-API-Key': 'demo-key-123'},
        'queryStringParameters': None
    }
    
    result = get_jobs(event, None)
    print(f"✅ Function call successful! Status: {result.get('statusCode')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
