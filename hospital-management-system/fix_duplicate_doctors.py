#!/usr/bin/env python3
"""
Fix duplicate doctor entries in database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import Availability, DoctorProfile

def fix_duplicate_doctors():
    print("Checking for duplicate doctors...")
    
    # Find all doctors named smith
    smith_doctors = User.objects.filter(
        user_type='doctor',
        username__icontains='smith'
    )
    
    print(f"Found {smith_doctors.count()} doctors with 'smith' in username:")
    for doctor in smith_doctors:
        print(f"- {doctor.username} (ID: {doctor.id})")
    
    if smith_doctors.count() > 1:
        # Keep the first one, remove others
        keep_doctor = smith_doctors.first()
        duplicate_doctors = smith_doctors.exclude(id=keep_doctor.id)
        
        for duplicate in duplicate_doctors:
            print(f"Removing duplicate doctor: {duplicate.username}")
            
            # Move availability slots to the main doctor
            Availability.objects.filter(doctor=duplicate).update(doctor=keep_doctor)
            
            # Remove duplicate doctor profile if exists
            try:
                duplicate.doctorprofile.delete()
            except:
                pass
            
            # Remove duplicate doctor
            duplicate.delete()
        
        print(f"✅ Kept only one Dr. Smith: {keep_doctor.username}")
    else:
        print("✅ No duplicate doctors found")

if __name__ == "__main__":
    fix_duplicate_doctors()