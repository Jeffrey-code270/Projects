import json
from typing import Dict, Any, Optional, List
from src.models.schemas import ErrorResponse

def create_success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key'
        },
        'body': json.dumps(data, default=str)
    }

def create_error_response(error: str, status_code: int = 500, details: str = None) -> Dict[str, Any]:
    error_response = ErrorResponse(
        error=error,
        code=status_code,
        details=details
    )
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key'
        },
        'body': json.dumps(error_response.dict())
    }

def create_validation_error_response(errors: List[str]) -> Dict[str, Any]:
    error_message = "Validation failed: " + "; ".join(errors)
    return create_error_response(error_message, 400)

def handle_cors_response(event: Dict[str, Any]) -> Dict[str, Any]:
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    return None
