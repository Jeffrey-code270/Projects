"""
Handler for POST /candidates endpoint
Creates a candidate and applies them to a job
"""

import os
from typing import Dict, Any
from src.services.greenhouse_client import GreenhouseClient
from src.utils.logger import get_logger
from src.utils.api_response import create_success_response, create_error_response, handle_cors_response
from src.utils.validation import validate_api_key, validate_request_body, validate_candidate_data
from src.utils.exceptions import ATSServiceError, AuthenticationError, ATSAPIError, ValidationError

logger = get_logger(__name__)

def create_candidate(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        cors_response = handle_cors_response(event)
        if cors_response:
            return cors_response
        
        if not validate_api_key(event):
            logger.warning("Unauthorized request - invalid API key")
            return create_error_response("Unauthorized", 401, "Invalid or missing API key")
        
        body = validate_request_body(event)
        candidate_data = validate_candidate_data(body)
        
        logger.info(f"Creating candidate for job {candidate_data.job_id}")
        
        try:
            client = GreenhouseClient()
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            return create_error_response("Authentication failed", 500, str(e))
        
        try:
            candidate_response = client.create_candidate(candidate_data)
            candidate_id = str(candidate_response.get('id'))
            logger.info(f"Successfully created candidate with ID: {candidate_id}")
        except ATSAPIError as e:
            logger.error(f"ATS API error creating candidate: {str(e)}")
            return create_error_response("Failed to create candidate in ATS", 502, str(e))
        except Exception as e:
            logger.error(f"Unexpected error creating candidate: {str(e)}")
            return create_error_response("Internal server error", 500, str(e))
        
        try:
            application_response = client.create_application(candidate_id, candidate_data.job_id)
            application_id = str(application_response.get('id'))
            logger.info(f"Successfully created application with ID: {application_id}")
        except ATSAPIError as e:
            logger.error(f"ATS API error creating application: {str(e)}")
            logger.warning(f"Application creation failed but candidate {candidate_id} was created")
            return create_error_response("Candidate created but failed to apply to job", 502, str(e))
        except Exception as e:
            logger.error(f"Unexpected error creating application: {str(e)}")
            return create_error_response("Candidate created but failed to apply to job", 502, str(e))
        
        success_response = {
            'message': 'Candidate created and applied successfully',
            'candidate_id': candidate_id,
            'application_id': application_id,
            'candidate': {
                'name': candidate_data.name,
                'email': candidate_data.email,
                'job_id': candidate_data.job_id
            }
        }
        
        logger.info(f"Successfully completed candidate creation and application")
        return create_success_response(success_response, 201)
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return create_error_response("Validation failed", 400, str(e))
    except ATSServiceError as e:
        logger.error(f"ATS service error: {str(e)}")
        return create_error_response("Service error", 500, str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_candidate: {str(e)}")
        return create_error_response("Internal server error", 500)
