from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    google_calendar_token = models.TextField(blank=True, null=True)
    
    def is_doctor(self):
        return self.user_type == 'doctor'
    
    def is_patient(self):
        return self.user_type == 'patient'