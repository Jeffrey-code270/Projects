import os
import requests
import base64
from typing import Dict, List, Optional, Any
from src.models.schemas import Job, Candidate, Application, JobStatus, ApplicationStatus
from src.utils.exceptions import ATSAPIError, AuthenticationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GreenhouseClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv('GREENHOUSE_API_KEY')
        self.base_url = base_url or os.getenv('GREENHOUSE_BASE_URL', 'https://harvest.greenhouse.io')
        
        if not self.api_key:
            raise AuthenticationError("Greenhouse API key is required")
        
        credentials = f"{self.api_key}:"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'User-Agent': 'ATS-Integration-Service/1.0'
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/{endpoint.lstrip('/')}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")
            
            if response.status_code >= 400:
                error_msg = f"API request failed: {response.status_code} {response.text}"
                logger.error(error_msg)
                raise ATSAPIError(error_msg, response.status_code)
            
            if response.status_code == 204:
                return {}
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise ATSAPIError(f"Request to Greenhouse API failed: {str(e)}")
    
    def get_jobs(self, status: Optional[str] = None, page: int = 1, per_page: int = 100) -> List[Job]:
        params = {
            'page': page,
            'per_page': per_page
        }
        
        if status:
            params['status'] = status
        
        try:
            response = self._make_request('GET', 'jobs', params=params)
            
            jobs = []
            for job_data in response:
                gh_status = job_data.get('status', '').upper()
                mapped_status = JobStatus.OPEN
                
                if gh_status == 'OPEN':
                    mapped_status = JobStatus.OPEN
                elif gh_status == 'CLOSED':
                    mapped_status = JobStatus.CLOSED
                elif gh_status == 'DRAFT':
                    mapped_status = JobStatus.DRAFT
                
                job = Job(
                    id=str(job_data['id']),
                    title=job_data.get('title', ''),
                    location=self._extract_location(job_data),
                    status=mapped_status,
                    external_url=job_data.get('absolute_url', '')
                )
                jobs.append(job)
            
            logger.info(f"Retrieved {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching jobs: {str(e)}")
            raise ATSAPIError(f"Failed to fetch jobs: {str(e)}")
    
    def create_candidate(self, candidate_data: Candidate) -> Dict[str, Any]:
        payload = {
            'first_name': candidate_data.name.split()[0] if candidate_data.name else '',
            'last_name': ' '.join(candidate_data.name.split()[1:]) if len(candidate_data.name.split()) > 1 else '',
            'email_addresses': [
                {
                    'value': candidate_data.email,
                    'type': 'work'
                }
            ],
            'phone_numbers': []
        }
        
        if candidate_data.phone:
            payload['phone_numbers'].append({
                'value': candidate_data.phone,
                'type': 'mobile'
            })
        
        if candidate_data.resume_url:
            payload['resume_url'] = candidate_data.resume_url
        
        try:
            response = self._make_request('POST', 'candidates', json=payload)
            logger.info(f"Created candidate with ID: {response.get('id')}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating candidate: {str(e)}")
            raise ATSAPIError(f"Failed to create candidate: {str(e)}")
    
    def create_application(self, candidate_id: str, job_id: str) -> Dict[str, Any]:
        payload = {
            'job_id': int(job_id),
            'candidate_id': int(candidate_id)
        }
        
        try:
            response = self._make_request('POST', 'applications', json=payload)
            logger.info(f"Created application for candidate {candidate_id} and job {job_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            raise ATSAPIError(f"Failed to create application: {str(e)}")
    
    def get_applications(self, job_id: Optional[str] = None, page: int = 1, per_page: int = 100) -> List[Application]:
        params = {
            'page': page,
            'per_page': per_page
        }
        
        endpoint = 'applications'
        if job_id:
            endpoint = f'jobs/{job_id}/applications'
        
        try:
            response = self._make_request('GET', endpoint, params=params)
            
            applications = []
            for app_data in response:
                gh_status = app_data.get('status', '').upper()
                mapped_status = ApplicationStatus.APPLIED
                
                if 'REJECT' in gh_status:
                    mapped_status = ApplicationStatus.REJECTED
                elif 'HIRE' in gh_status:
                    mapped_status = ApplicationStatus.HIRED
                elif 'SCREEN' in gh_status:
                    mapped_status = ApplicationStatus.SCREENING
                else:
                    mapped_status = ApplicationStatus.APPLIED
                
                candidate = app_data.get('candidate', {})
                candidate_name = f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip()
                candidate_email = ''
                
                if 'email_addresses' in candidate and candidate['email_addresses']:
                    candidate_email = candidate['email_addresses'][0].get('value', '')
                
                application = Application(
                    id=str(app_data['id']),
                    candidate_name=candidate_name,
                    email=candidate_email,
                    status=mapped_status
                )
                applications.append(application)
            
            logger.info(f"Retrieved {len(applications)} applications")
            return applications
            
        except Exception as e:
            logger.error(f"Error fetching applications: {str(e)}")
            raise ATSAPIError(f"Failed to fetch applications: {str(e)}")
    
    def _extract_location(self, job_data: Dict[str, Any]) -> str:
        locations = job_data.get('offices', [])
        if locations:
            return locations[0].get('name', 'Remote')
        return 'Remote'
