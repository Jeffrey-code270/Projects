#!/usr/bin/env python3
"""
Demo script for Hospital Management System
Creates sample data for demonstration
"""
import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import Availability

def create_demo_data():
    print("Creating demo data for HMS...")
    
    # Create a demo doctor
    doctor, created = User.objects.get_or_create(
        username='dr_smith',
        defaults={
            'email': 'dr.smith@hospital.com',
            'user_type': 'doctor',
            'first_name': 'John',
            'last_name': 'Smith'
        }
    )
    if created:
        doctor.set_password('demo123')
        doctor.save()
        print("✅ Created demo doctor: dr_smith (password: demo123)")
    
    # Create a demo patient
    patient, created = User.objects.get_or_create(
        username='patient_doe',
        defaults={
            'email': 'patient.doe@email.com',
            'user_type': 'patient',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
    )
    if created:
        patient.set_password('demo123')
        patient.save()
        print("✅ Created demo patient: patient_doe (password: demo123)")
    
    # Create some availability slots for the doctor
    today = datetime.now().date()
    
    # Create slots for next 5 days
    for i in range(1, 6):
        date = today + timedelta(days=i)
        
        # Morning slots
        for hour in [9, 10, 11]:
            availability, created = Availability.objects.get_or_create(
                doctor=doctor,
                date=date,
                start_time=f"{hour}:00",
                defaults={'end_time': f"{hour}:30"}
            )
            if created:
                print(f"✅ Created availability: {date} {hour}:00-{hour}:30")
        
        # Afternoon slots
        for hour in [14, 15, 16]:
            availability, created = Availability.objects.get_or_create(
                doctor=doctor,
                date=date,
                start_time=f"{hour}:00",
                defaults={'end_time': f"{hour}:30"}
            )
            if created:
                print(f"✅ Created availability: {date} {hour}:00-{hour}:30")
    
    print("\n🎉 Demo data created successfully!")
    print("\nDemo Accounts:")
    print("Doctor Login: dr_smith / demo123")
    print("Patient Login: patient_doe / demo123")
    print("\nStart the server with: python3 manage.py runserver")
    print("Visit: http://localhost:8000")

if __name__ == "__main__":
    create_demo_data()