
#!/usr/bin/env python3
"""
Test script for ATS Integration Service API endpoints
This script simulates the Lambda function calls to test our handlers
"""

import json
import sys
import os
from unittest.mock import Mock, patch

# Add current directory and src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))


from src.handlers.jobs import get_jobs
from src.handlers.candidates import create_candidate
from src.handlers.applications import get_applications

def test_get_jobs():
    """Test GET /jobs endpoint"""
    print("Testing GET /jobs endpoint...")
    
    # Mock event for jobs endpoint
    event = {
        'httpMethod': 'GET',
        'path': '/jobs',
        'headers': {
            'X-API-Key': 'demo-key-123'
        },
        'queryStringParameters': {
            'status': 'OPEN',
            'page': '1',
            'per_page': '10'
        }
    }
    
    context = Mock()
    
    try:
        response = get_jobs(event, context)
        print("✅ GET /jobs test passed")
        print(f"Response status: {response['statusCode']}")
        
        if response['statusCode'] == 200:
            body = json.loads(response['body'])
            print(f"Response body: {json.dumps(body, indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ GET /jobs test failed: {str(e)}")
        return False

def test_create_candidate():
    """Test POST /candidates endpoint"""
    print("\nTesting POST /candidates endpoint...")
    
    # Mock event for candidate creation
    event = {
        'httpMethod': 'POST',
        'path': '/candidates',
        'headers': {
            'Content-Type': 'application/json',
            'X-API-Key': 'demo-key-123'
        },
        'body': json.dumps({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'job_id': '12345'
        })
    }
    
    context = Mock()
    
    try:
        response = create_candidate(event, context)
        print("✅ POST /candidates test passed")
        print(f"Response status: {response['statusCode']}")
        
        if response['statusCode'] in [200, 201]:
            body = json.loads(response['body'])
            print(f"Response body: {json.dumps(body, indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ POST /candidates test failed: {str(e)}")
        return False

def test_get_applications():
    """Test GET /applications endpoint"""
    print("\nTesting GET /applications endpoint...")
    
    # Mock event for applications endpoint
    event = {
        'httpMethod': 'GET',
        'path': '/applications',
        'headers': {
            'X-API-Key': 'demo-key-123'
        },
        'queryStringParameters': {
            'job_id': '12345',
            'page': '1',
            'per_page': '10'
        }
    }
    
    context = Mock()
    
    try:
        response = get_applications(event, context)
        print("✅ GET /applications test passed")
        print(f"Response status: {response['statusCode']}")
        
        if response['statusCode'] == 200:
            body = json.loads(response['body'])
            print(f"Response body: {json.dumps(body, indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ GET /applications test failed: {str(e)}")
        return False

def test_invalid_api_key():
    """Test with invalid API key"""
    print("\nTesting invalid API key...")
    
    event = {
        'httpMethod': 'GET',
        'path': '/jobs',
        'headers': {
            'X-API-Key': 'invalid-key'
        }
    }
    
    context = Mock()
    
    try:
        response = get_jobs(event, context)
        if response['statusCode'] == 401:
            print("✅ Invalid API key test passed")
            return True
        else:
            print(f"❌ Expected 401, got {response['statusCode']}")
            return False
    except Exception as e:
        print(f"❌ Invalid API key test failed: {str(e)}")
        return False

def test_cors_preflight():
    """Test CORS preflight request"""
    print("\nTesting CORS preflight...")
    
    event = {
        'httpMethod': 'OPTIONS',
        'path': '/jobs',
        'headers': {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type,X-API-Key'
        }
    }
    
    context = Mock()
    
    try:
        response = get_jobs(event, context)
        if response['statusCode'] == 200:
            print("✅ CORS preflight test passed")
            return True
        else:
            print(f"❌ Expected 200, got {response['statusCode']}")
            return False
    except Exception as e:
        print(f"❌ CORS preflight test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting ATS Integration Service API Tests\n")
    
    tests = [
        test_cors_preflight,
        test_invalid_api_key,
        test_get_jobs,
        test_create_candidate,
        test_get_applications
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
