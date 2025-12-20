"""
Handler for GET /applications endpoint
Returns list of applications for a given job
"""

import os
from typing import Dict, Any
from src.services.greenhouse_client import GreenhouseClient
from src.utils.logger import get_logger
from src.utils.api_response import create_success_response, create_error_response, handle_cors_response
from src.utils.validation import validate_api_key, validate_query_parameters
from src.utils.exceptions import ATSServiceError, AuthenticationError, ATSAPIError, ValidationError
from src.models.schemas import PaginatedApplicationsResponse

logger = get_logger(__name__)

def get_applications(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        cors_response = handle_cors_response(event)
        if cors_response:
            return cors_response
        
        if not validate_api_key(event):
            logger.warning("Unauthorized request - invalid API key")
            return create_error_response("Unauthorized", 401, "Invalid or missing API key")
        
        validated_params = validate_query_parameters(event)
        page = validated_params['page']
        per_page = validated_params['per_page']
        job_id = validated_params.get('job_id')
        
        if not job_id:
            logger.warning("job_id query parameter is required for applications endpoint")
            return create_error_response("Bad Request", 400, "job_id query parameter is required")
        
        logger.info(f"Fetching applications for job {job_id} - page: {page}, per_page: {per_page}")
        
        try:
            client = GreenhouseClient()
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            return create_error_response("Authentication failed", 500, str(e))
        
        try:
            applications = client.get_applications(job_id=job_id, page=page, per_page=per_page)
        except ATSAPIError as e:
            logger.error(f"ATS API error: {str(e)}")
            return create_error_response("Failed to fetch applications from ATS", 502, str(e))
        except Exception as e:
            logger.error(f"Unexpected error fetching applications: {str(e)}")
            return create_error_response("Internal server error", 500, str(e))
        
        total = len(applications) + (page - 1) * per_page
        
        response_data = PaginatedApplicationsResponse(
            applications=applications,
            total=total,
            page=page,
            per_page=per_page
        )
        
        logger.info(f"Successfully returned {len(applications)} applications for job {job_id}")
        return create_success_response(response_data.dict())
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return create_error_response("Validation failed", 400, str(e))
    except ATSServiceError as e:
        logger.error(f"ATS service error: {str(e)}")
        return create_error_response("Service error", 500, str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_applications: {str(e)}")
        return create_error_response("Internal server error", 500)
