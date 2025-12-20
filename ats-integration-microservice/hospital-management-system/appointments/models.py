from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Specialties"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'doctor'})
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    years_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialty}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    medical_history = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Patient"

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'doctor'})
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    slot_type = models.CharField(max_length=20, choices=[
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency')
    ], default='consultation')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"Dr. {self.doctor.username} - {self.date} {self.start_time}-{self.end_time}"
    
    @property
    def is_available(self):
        return not self.is_booked and datetime.combine(self.date, self.start_time) > datetime.now()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} -> Dr. {self.availability.doctor.username} on {self.availability.date}"
    
    @property
    def total_fee(self):
        try:
            return self.availability.doctor.doctorprofile.consultation_fee
        except:
            return 100.00

class MedicalRecord(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Record for {self.booking}"