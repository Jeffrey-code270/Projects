#!/usr/bin/env python3
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import Availability, Specialty, DoctorProfile

def create_demo_data():
    # Create specialties
    cardiology, _ = Specialty.objects.get_or_create(name='Cardiology')
    dermatology, _ = Specialty.objects.get_or_create(name='Dermatology')
    neurology, _ = Specialty.objects.get_or_create(name='Neurology')
    
    # Create doctors
    doctors_data = [
        ('dr_smith', 'dr.smith@hospital.com', 'John', 'Smith', cardiology, 150.00),
        ('dr_johnson', 'dr.johnson@hospital.com', 'Sarah', 'Johnson', dermatology, 120.00),
        ('dr_williams', 'dr.williams@hospital.com', 'Michael', 'Williams', neurology, 200.00)
    ]
    
    for username, email, first, last, specialty, fee in doctors_data:
        doctor, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'user_type': 'doctor', 'first_name': first, 'last_name': last}
        )
        if created:
            doctor.set_password('demo123')
            doctor.save()
        
        DoctorProfile.objects.get_or_create(
            user=doctor,
            defaults={'specialty': specialty, 'consultation_fee': fee, 'license_number': f'MD{doctor.id}'}
        )
    
    # Create patients
    for username, email in [('patient_doe', 'patient.doe@email.com'), ('patient_brown', 'patient.brown@email.com')]:
        patient, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'user_type': 'patient'}
        )
        if created:
            patient.set_password('demo123')
            patient.save()
    
    # Create availability slots
    today = datetime.now().date()
    for doctor in User.objects.filter(user_type='doctor'):
        for i in range(1, 6):
            date = today + timedelta(days=i)
            for hour in [9, 10, 11, 14, 15, 16]:
                Availability.objects.get_or_create(
                    doctor=doctor, date=date, start_time=f"{hour}:00",
                    defaults={'end_time': f"{hour}:30"}
                )
    
    print("Demo data created! Login: dr_smith/demo123, patient_doe/demo123")

if __name__ == "__main__":
    create_demo_data()