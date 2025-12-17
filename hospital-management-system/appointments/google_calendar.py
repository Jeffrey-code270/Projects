from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from django.conf import settings
import json
from datetime import datetime, timedelta

def get_google_calendar_service(user):
    """Get Google Calendar service for a user"""
    if not user.google_calendar_token:
        return None
    
    try:
        token_data = json.loads(user.google_calendar_token)
        creds = Credentials.from_authorized_user_info(token_data)
        
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            user.google_calendar_token = creds.to_json()
            user.save()
        
        return build('calendar', 'v3', credentials=creds)
    except:
        return None

def create_calendar_event(booking):
    """Create calendar event for both doctor and patient"""
    doctor_service = get_google_calendar_service(booking.availability.doctor)
    patient_service = get_google_calendar_service(booking.patient)
    
    start_datetime = datetime.combine(
        booking.availability.date,
        booking.availability.start_time
    )
    end_datetime = datetime.combine(
        booking.availability.date,
        booking.availability.end_time
    )
    
    event = {
        'summary': f'Medical Appointment - Dr. {booking.availability.doctor.username} & {booking.patient.username}',
        'description': f'Appointment between Dr. {booking.availability.doctor.username} and {booking.patient.username}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': booking.availability.doctor.email},
            {'email': booking.patient.email},
        ],
    }
    
    event_id = None
    
    # Create event in doctor's calendar
    if doctor_service:
        try:
            doctor_event = doctor_service.events().insert(calendarId='primary', body=event).execute()
            event_id = doctor_event.get('id')
        except:
            pass
    
    # Create event in patient's calendar
    if patient_service:
        try:
            patient_service.events().insert(calendarId='primary', body=event).execute()
        except:
            pass
    
    return event_id

def get_oauth_flow():
    """Get OAuth flow for Google Calendar authorization"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8000/appointments/google-callback/"]
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = "http://localhost:8000/appointments/google-callback/"
    return flow