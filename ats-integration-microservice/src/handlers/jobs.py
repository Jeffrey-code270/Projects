"""
Handler for GET /jobs endpoint
Returns list of open jobs from Greenhouse ATS
"""

import os
from typing import Dict, Any
from src.services.greenhouse_client import GreenhouseClient
from src.utils.logger import get_logger
from src.utils.api_response import create_success_response, create_error_response, handle_cors_response
from src.utils.validation import validate_api_key, validate_query_parameters, validate_job_status_parameter
from src.utils.exceptions import ATSServiceError, AuthenticationError, ATSAPIError, ValidationError
from src.models.schemas import PaginatedJobsResponse

logger = get_logger(__name__)

def get_jobs(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
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
        status = validate_job_status_parameter(event)
        
        logger.info(f"Fetching jobs - page: {page}, per_page: {per_page}, status: {status}")
        
        try:
            client = GreenhouseClient()
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            return create_error_response("Authentication failed", 500, str(e))
        
        try:
            jobs = client.get_jobs(status=status, page=page, per_page=per_page)
        except ATSAPIError as e:
            logger.error(f"ATS API error: {str(e)}")
            return create_error_response("Failed to fetch jobs from ATS", 502, str(e))
        except Exception as e:
            logger.error(f"Unexpected error fetching jobs: {str(e)}")
            return create_error_response("Internal server error", 500, str(e))
        
        total = len(jobs) + (page - 1) * per_page
        
        response_data = PaginatedJobsResponse(
            jobs=jobs,
            total=total,
            page=page,
            per_page=per_page
        )
        
        logger.info(f"Successfully returned {len(jobs)} jobs")
        return create_success_response(response_data.dict())
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return create_error_response("Validation failed", 400, str(e))
    except ATSServiceError as e:
        logger.error(f"ATS service error: {str(e)}")
        return create_error_response("Service error", 500, str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_jobs: {str(e)}")
        return create_error_response("Internal server error", 500)
