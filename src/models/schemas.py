from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

class JobStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    DRAFT = "DRAFT"

class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    REJECTED = "REJECTED"
    HIRED = "HIRED"

class Job(BaseModel):
    id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    location: str = Field(..., description="Job location")
    status: JobStatus = Field(..., description="Job status")
    external_url: str = Field(..., description="External job URL")

class Candidate(BaseModel):
    name: str = Field(..., description="Candidate full name")
    email: EmailStr = Field(..., description="Candidate email address")
    phone: Optional[str] = Field(None, description="Candidate phone number")
    resume_url: Optional[str] = Field(None, description="URL to candidate's resume")
    job_id: str = Field(..., description="Job ID to apply for")

class Application(BaseModel):
    id: str = Field(..., description="Application ID")
    candidate_name: str = Field(..., description="Candidate full name")
    email: str = Field(..., description="Candidate email")
    status: ApplicationStatus = Field(..., description="Application status")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    code: int = Field(..., description="HTTP status code")
    details: Optional[str] = Field(None, description="Additional error details")

class PaginatedJobsResponse(BaseModel):
    jobs: List[Job]
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Jobs per page")

class PaginatedApplicationsResponse(BaseModel):
    applications: List[Application]
    total: int = Field(..., description="Total number of applications")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Applications per page")
