from django import forms
from .models import Availability, Booking, DoctorProfile, PatientProfile

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time', 'slot_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'slot_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['symptoms']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your symptoms or reason for visit...'
            })
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialty', 'license_number', 'years_experience', 'consultation_fee', 'bio']
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'phone', 'emergency_contact', 'medical_history']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }