#!/usr/bin/env python3
"""
Check booking and availability status
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from appointments.models import Availability, Booking

def check_status():
    print("Checking booking and availability status...\n")
    
    # Check all availabilities
    availabilities = Availability.objects.all().order_by('date', 'start_time')
    print("All Availability Slots:")
    for avail in availabilities:
        print(f"ID: {avail.id} | Dr. {avail.doctor.username} | {avail.date} {avail.start_time} | Booked: {avail.is_booked}")
    
    print("\nAll Bookings:")
    bookings = Booking.objects.all().order_by('-booked_at')
    for booking in bookings:
        print(f"ID: {booking.id} | Patient: {booking.patient.username} | Availability ID: {booking.availability.id} | Status: {booking.status}")
    
    print("\nCancelled Bookings with their Availability Status:")
    cancelled_bookings = Booking.objects.filter(status='cancelled')
    for booking in cancelled_bookings:
        avail = booking.availability
        print(f"Booking ID: {booking.id} | Availability ID: {avail.id} | is_booked: {avail.is_booked}")

if __name__ == "__main__":
    check_status()