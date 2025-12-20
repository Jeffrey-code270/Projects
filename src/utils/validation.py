import json
import os
from typing import Dict, Any, Optional, List
import re
from src.models.schemas import Candidate
from src.utils.exceptions import ValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

def validate_api_key(event: Dict[str, Any]) -> bool:
    expected_api_key = os.getenv('API_KEY', 'demo-key-123')
    provided_key = event.get('headers', {}).get('X-API-Key') or event.get('headers', {}).get('x-api-key')
    
    if not provided_key:
        logger.warning("API key missing from request")
        return False
    
    if provided_key != expected_api_key:
        logger.warning("Invalid API key provided")
        return False
    
    return True

def validate_request_body(event: Dict[str, Any]) -> Dict[str, Any]:
    if not event.get('body'):
        raise ValidationError("Request body is required")
    
    try:
        body = json.loads(event['body'])
        return body
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in request body: {str(e)}")

def validate_candidate_data(body: Dict[str, Any]) -> Candidate:
    errors = []
    
    required_fields = ['name', 'email', 'job_id']
    for field in required_fields:
        if field not in body or not body[field]:
            errors.append(f"Field '{field}' is required")
    
    if 'email' in body and body['email']:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, body['email']):
            errors.append("Invalid email format")
    
    if 'phone' in body and body['phone']:
        phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
        if not re.match(phone_pattern, body['phone'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            errors.append("Invalid phone format")
    
    if 'resume_url' in body and body['resume_url']:
        if not (body['resume_url'].startswith('http://') or body['resume_url'].startswith('https://')):
            errors.append("Resume URL must be a valid HTTP/HTTPS URL")
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    return Candidate(**body)

def validate_query_parameters(event: Dict[str, Any]) -> Dict[str, Any]:
    params = event.get('queryStringParameters') or {}
    validated_params = {}
    
    if 'job_id' in params:
        if not params['job_id'].strip():
            raise ValidationError("job_id cannot be empty")
        validated_params['job_id'] = params['job_id']
    
    if 'page' in params:
        try:
            page = int(params['page'])
            if page < 1:
                raise ValidationError("page must be greater than 0")
            validated_params['page'] = page
        except ValueError:
            raise ValidationError("page must be a valid integer")
    else:
        validated_params['page'] = 1
    
    if 'per_page' in params:
        try:
            per_page = int(params['per_page'])
            if per_page < 1 or per_page > 100:
                raise ValidationError("per_page must be between 1 and 100")
            validated_params['per_page'] = per_page
        except ValueError:
            raise ValidationError("per_page must be a valid integer")
    else:
        validated_params['per_page'] = 50
    
    return validated_params

def validate_job_status_parameter(event: Dict[str, Any]) -> Optional[str]:
    params = event.get('queryStringParameters') or {}
    status = params.get('status')
    
    if status:
        valid_statuses = ['OPEN', 'CLOSED', 'DRAFT']
        if status.upper() not in valid_statuses:
            raise ValidationError(f"status must be one of: {', '.join(valid_statuses)}")
        return status.upper()
    
    return None
