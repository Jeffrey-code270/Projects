from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Availability, Booking, DoctorProfile, PatientProfile, Specialty
from .forms import AvailabilityForm, BookingForm, DoctorProfileForm, PatientProfileForm
from .google_calendar import create_calendar_event
import requests
from django.conf import settings

@login_required
def dashboard(request):
    if request.user.is_doctor():
        # Get or create doctor profile
        profile, created = DoctorProfile.objects.get_or_create(user=request.user)
        
        availabilities = Availability.objects.filter(doctor=request.user).order_by('-date', '-start_time')
        bookings = Booking.objects.filter(availability__doctor=request.user).order_by('-booked_at')
        
        # Statistics
        total_slots = availabilities.count()
        booked_slots = availabilities.filter(is_booked=True).count()
        upcoming_appointments = bookings.filter(
            availability__date__gte=timezone.now().date(),
            status='confirmed'
        ).count()
        
        return render(request, 'appointments/doctor_dashboard.html', {
            'profile': profile,
            'availabilities': availabilities[:10],  # Recent 10
            'bookings': bookings[:10],  # Recent 10
            'stats': {
                'total_slots': total_slots,
                'booked_slots': booked_slots,
                'upcoming_appointments': upcoming_appointments
            }
        })
    else:
        # Get or create patient profile
        profile, created = PatientProfile.objects.get_or_create(user=request.user)
        
        # Get doctors with available slots
        available_doctors = Availability.objects.filter(
            is_booked=False,
            date__gte=timezone.now().date()
        ).select_related('doctor__doctorprofile__specialty').values(
            'doctor__username', 
            'doctor__id',
            'doctor__doctorprofile__specialty__name',
            'doctor__doctorprofile__consultation_fee'
        ).distinct()
        
        # Patient's bookings
        my_bookings = Booking.objects.filter(patient=request.user).order_by('-booked_at')
        
        return render(request, 'appointments/patient_dashboard.html', {
            'profile': profile,
            'doctors': available_doctors,
            'my_bookings': my_bookings[:5]  # Recent 5
        })

@login_required
def create_availability(request):
    if not request.user.is_doctor():
        messages.error(request, "Only doctors can create availability.")
        return redirect('appointments:dashboard')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            availability.save()
            messages.success(request, "Availability created successfully!")
            return redirect('appointments:dashboard')
    else:
        form = AvailabilityForm()
    
    return render(request, 'appointments/create_availability.html', {'form': form})

@login_required
def book_appointment(request, availability_id):
    if not request.user.is_patient():
        messages.error(request, "Only patients can book appointments.")
        return redirect('appointments:dashboard')
    
    availability = get_object_or_404(Availability, id=availability_id, is_booked=False)
    
    if request.method == 'GET':
        if not availability.is_available:
            messages.error(request, "This slot is no longer available.")
            return redirect('appointments:dashboard')
        
        form = BookingForm()
        return render(request, 'appointments/confirm_booking.html', {
            'availability': availability,
            'form': form
        })
    
    # Handle POST for actual booking
    form = BookingForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            availability = get_object_or_404(
                Availability.objects.select_for_update(),
                id=availability_id,
                is_booked=False
            )
            
            if not availability.is_available:
                messages.error(request, "This slot is no longer available.")
                return redirect('appointments:dashboard')
            
            # Check if booking already exists
            if Booking.objects.filter(availability=availability).exists():
                messages.error(request, "This slot has already been booked.")
                return redirect('appointments:dashboard')
            
            # Create booking
            booking = form.save(commit=False)
            booking.patient = request.user
            booking.availability = availability
            booking.save()
            
            # Mark availability as booked
            availability.is_booked = True
            availability.save()
            
            # Create Google Calendar events
            try:
                event_id = create_calendar_event(booking)
                booking.google_event_id = event_id
                booking.save()
            except Exception as e:
                messages.warning(request, "Appointment booked but calendar event creation failed.")
            
            # Send confirmation email
            try:
                email_data = {
                    'action': 'BOOKING_CONFIRMATION',
                    'to_email': request.user.email,
                    'patient_name': request.user.username,
                    'doctor_name': availability.doctor.username,
                    'date': str(availability.date),
                    'time': str(availability.start_time),
                    'fee': str(booking.total_fee),
                    'symptoms': booking.symptoms
                }
                requests.post(settings.EMAIL_SERVICE_URL, json=email_data, timeout=5)
            except:
                pass
            
            messages.success(request, f"Appointment booked with Dr. {availability.doctor.username}!")
            return redirect('appointments:dashboard')
    
    return render(request, 'appointments/confirm_booking.html', {
        'availability': availability,
        'form': form
    })

@login_required
def doctor_profile(request):
    if not request.user.is_doctor():
        messages.error(request, "Access denied.")
        return redirect('appointments:dashboard')
    
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('appointments:dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    
    return render(request, 'appointments/doctor_profile.html', {'form': form})

@login_required
def patient_profile(request):
    if not request.user.is_patient():
        messages.error(request, "Access denied.")
        return redirect('appointments:dashboard')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('appointments:dashboard')
    else:
        form = PatientProfileForm(instance=profile)
    
    return render(request, 'appointments/patient_profile.html', {'form': form})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if not (request.user == booking.patient or request.user == booking.availability.doctor):
        messages.error(request, "Access denied.")
        return redirect('appointments:dashboard')
    
    if booking.status != 'confirmed':
        messages.error(request, "Cannot cancel this booking.")
        return redirect('appointments:dashboard')
    
    # Cancel booking
    booking.status = 'cancelled'
    booking.save()
    
    # Free up the slot
    booking.availability.is_booked = False
    booking.availability.save()
    
    messages.success(request, "Booking cancelled successfully!")
    return redirect('appointments:dashboard')

@login_required
def doctor_availability_api(request, doctor_id):
    slots = Availability.objects.filter(
        doctor_id=doctor_id,
        is_booked=False,
        date__gte=timezone.now().date()
    ).select_related('doctor__doctorprofile').values(
        'id', 'date', 'start_time', 'end_time', 'slot_type',
        'doctor__doctorprofile__consultation_fee'
    )
    
    return JsonResponse({'slots': list(slots)})