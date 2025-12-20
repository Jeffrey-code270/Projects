#!/usr/bin/env python3
"""
Create availability slots for all doctors
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from appointments.models import Availability

def create_slots_for_all_doctors():
    print("Creating availability slots for all doctors...")
    
    doctors = User.objects.filter(user_type='doctor')
    today = datetime.now().date()
    
    for doctor in doctors:
        print(f"\nCreating slots for Dr. {doctor.username}...")
        
        for i in range(1, 6):  # Next 5 days
            date = today + timedelta(days=i)
            
            # Morning slots
            for hour in [9, 10, 11]:
                availability, created = Availability.objects.get_or_create(
                    doctor=doctor,
                    date=date,
                    start_time=f"{hour}:00",
                    defaults={
                        'end_time': f"{hour}:30",
                        'slot_type': 'consultation'
                    }
                )
                if created:
                    print(f"✅ Created slot: {date} {hour}:00-{hour}:30")
            
            # Afternoon slots
            for hour in [14, 15, 16]:
                availability, created = Availability.objects.get_or_create(
                    doctor=doctor,
                    date=date,
                    start_time=f"{hour}:00",
                    defaults={
                        'end_time': f"{hour}:30",
                        'slot_type': 'consultation'
                    }
                )
                if created:
                    print(f"✅ Created slot: {date} {hour}:00-{hour}:30")
    
    print("\n🎉 All doctors now have availability slots!")

if __name__ == "__main__":
    create_slots_for_all_doctors()