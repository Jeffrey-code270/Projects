#!/usr/bin/env python3
"""
Update existing doctors with complete profile information
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import DoctorProfile, Specialty

def update_existing_doctors():
    print("Updating existing doctor profiles...")
    
    # Update dr_smith if exists
    try:
        doctor = User.objects.get(username='dr_smith')
        specialty = Specialty.objects.get(name='Cardiology')
        
        profile, created = DoctorProfile.objects.get_or_create(
            user=doctor,
            defaults={
                'specialty': specialty,
                'license_number': 'MD12345',
                'years_experience': 15,
                'consultation_fee': 150.00,
                'bio': 'Experienced cardiologist specializing in heart disease prevention and treatment.'
            }
        )
        
        if not created:
            # Update existing profile
            profile.specialty = specialty
            profile.license_number = 'MD12345'
            profile.years_experience = 15
            profile.consultation_fee = 150.00
            profile.bio = 'Experienced cardiologist specializing in heart disease prevention and treatment.'
            profile.save()
        
        print(f"✅ Updated Dr. Smith profile - Cardiology, $150")
        
    except User.DoesNotExist:
        print("Dr. Smith not found")
    
    # Check and update other doctors
    doctors_to_update = [
        {
            'username': 'dr_johnson',
            'specialty': 'Dermatology',
            'license': 'MD67890',
            'experience': 8,
            'fee': 120.00,
            'bio': 'Dermatologist focused on skin cancer prevention and cosmetic procedures.'
        },
        {
            'username': 'dr_williams', 
            'specialty': 'Neurology',
            'license': 'MD11111',
            'experience': 20,
            'fee': 200.00,
            'bio': 'Neurologist specializing in brain disorders and neurological conditions.'
        }
    ]
    
    for doc_data in doctors_to_update:
        try:
            doctor = User.objects.get(username=doc_data['username'])
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
            
            if not created:
                # Update existing profile
                profile.specialty = specialty
                profile.license_number = doc_data['license']
                profile.years_experience = doc_data['experience']
                profile.consultation_fee = doc_data['fee']
                profile.bio = doc_data['bio']
                profile.save()
            
            print(f"✅ Updated Dr. {doctor.username} profile - {doc_data['specialty']}, ${doc_data['fee']}")
            
        except User.DoesNotExist:
            print(f"Dr. {doc_data['username']} not found")
    
    print("\n🎉 All doctor profiles updated!")
    print("\nDoctors now have:")
    print("- Dr. Smith: Cardiology - $150")
    print("- Dr. Johnson: Dermatology - $120") 
    print("- Dr. Williams: Neurology - $200")

if __name__ == "__main__":
    update_existing_doctors()