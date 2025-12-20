#!/usr/bin/env python3
"""
Enhanced demo script for Hospital Management System
Creates comprehensive sample data
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import Availability, Specialty, DoctorProfile, PatientProfile

def create_enhanced_demo_data():
    print("Creating enhanced demo data for HMS...")
    
    # Create specialties
    specialties = [
        ('Cardiology', 'Heart and cardiovascular system'),
        ('Dermatology', 'Skin, hair, and nail conditions'),
        ('Neurology', 'Brain and nervous system disorders'),
        ('Orthopedics', 'Bone, joint, and muscle problems'),
        ('Pediatrics', 'Medical care for children')
    ]
    
    for name, desc in specialties:
        specialty, created = Specialty.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        if created:
            print(f"✅ Created specialty: {name}")
    
    # Create enhanced doctors
    doctors_data = [
        {
            'username': 'dr_smith',
            'email': 'dr.smith@hospital.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'specialty': 'Cardiology',
            'license': 'MD12345',
            'experience': 15,
            'fee': 150.00,
            'bio': 'Experienced cardiologist specializing in heart disease prevention and treatment.'
        },
        {
            'username': 'dr_johnson',
            'email': 'dr.johnson@hospital.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'specialty': 'Dermatology',
            'license': 'MD67890',
            'experience': 8,
            'fee': 120.00,
            'bio': 'Dermatologist focused on skin cancer prevention and cosmetic procedures.'
        },
        {
            'username': 'dr_williams',
            'email': 'dr.williams@hospital.com',
            'first_name': 'Michael',
            'last_name': 'Williams',
            'specialty': 'Neurology',
            'license': 'MD11111',
            'experience': 20,
            'fee': 200.00,
            'bio': 'Neurologist specializing in brain disorders and neurological conditions.'
        }
    ]
    
    for doc_data in doctors_data:
        doctor, created = User.objects.get_or_create(
            username=doc_data['username'],
            defaults={
                'email': doc_data['email'],
                'user_type': 'doctor',
                'first_name': doc_data['first_name'],
                'last_name': doc_data['last_name']
            }
        )
        if created:
            doctor.set_password('demo123')
            doctor.save()
            print(f"✅ Created doctor: {doc_data['username']}")
        
        # Create doctor profile
        specialty = Specialty.objects.get(name=doc_data['specialty'])
        profile, created = DoctorProfile.objects.get_or_create(
            user=doctor,
            defaults={
                'specialty': specialty,
                'license_number': doc_data['license'],
                'years_experience': doc_data['experience'],
                'consultation_fee': doc_data['fee'],
                'bio': doc_data['bio']
            }
        )
        if created:
            print(f"✅ Created profile for Dr. {doc_data['last_name']}")
    
    # Create enhanced patients
    patients_data = [
        {
            'username': 'patient_doe',
            'email': 'jane.doe@email.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'dob': '1990-05-15',
            'phone': '+1-555-0123',
            'emergency': 'John Doe - +1-555-0124',
            'history': 'No major medical history. Regular checkups.'
        },
        {
            'username': 'patient_brown',
            'email': 'bob.brown@email.com',
            'first_name': 'Bob',
            'last_name': 'Brown',
            'dob': '1985-12-03',
            'phone': '+1-555-0125',
            'emergency': 'Alice Brown - +1-555-0126',
            'history': 'Hypertension, managed with medication.'
        }
    ]
    
    for pat_data in patients_data:
        patient, created = User.objects.get_or_create(
            username=pat_data['username'],
            defaults={
                'email': pat_data['email'],
                'user_type': 'patient',
                'first_name': pat_data['first_name'],
                'last_name': pat_data['last_name']
            }
        )
        if created:
            patient.set_password('demo123')
            patient.save()
            print(f"✅ Created patient: {pat_data['username']}")
        
        # Create patient profile
        profile, created = PatientProfile.objects.get_or_create(
            user=patient,
            defaults={
                'date_of_birth': pat_data['dob'],
                'phone': pat_data['phone'],
                'emergency_contact': pat_data['emergency'],
                'medical_history': pat_data['history']
            }
        )
        if created:
            print(f"✅ Created profile for {pat_data['first_name']} {pat_data['last_name']}")
    
    # Create diverse availability slots
    doctors = User.objects.filter(user_type='doctor')
    today = datetime.now().date()
    
    slot_types = ['consultation', 'follow_up', 'emergency']
    
    for doctor in doctors:
        for i in range(1, 8):  # Next 7 days
            date = today + timedelta(days=i)
            
            # Morning slots
            for hour in [9, 10, 11]:
                for slot_type in slot_types[:2]:  # consultation and follow_up
                    availability, created = Availability.objects.get_or_create(
                        doctor=doctor,
                        date=date,
                        start_time=f"{hour}:00",
                        slot_type=slot_type,
                        defaults={'end_time': f"{hour}:30"}
                    )
                    if created:
                        print(f"✅ Created {slot_type} slot: Dr. {doctor.username} - {date} {hour}:00")
            
            # Afternoon slots
            for hour in [14, 15, 16]:
                availability, created = Availability.objects.get_or_create(
                    doctor=doctor,
                    date=date,
                    start_time=f"{hour}:00",
                    slot_type='consultation',
                    defaults={'end_time': f"{hour}:30"}
                )
                if created:
                    print(f"✅ Created consultation slot: Dr. {doctor.username} - {date} {hour}:00")
    
    print("\n🎉 Enhanced demo data created successfully!")
    print("\nDemo Accounts:")
    print("Doctors:")
    print("- dr_smith / demo123 (Cardiology - $150)")
    print("- dr_johnson / demo123 (Dermatology - $120)")
    print("- dr_williams / demo123 (Neurology - $200)")
    print("\nPatients:")
    print("- patient_doe / demo123")
    print("- patient_brown / demo123")
    print("\nFeatures:")
    print("- Doctor specialties and profiles")
    print("- Patient profiles with medical history")
    print("- Different slot types (consultation, follow-up)")
    print("- Consultation fees")
    print("- Booking with symptoms")
    print("- Cancellation system")

if __name__ == "__main__":
    create_enhanced_demo_data()