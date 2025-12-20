from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-availability/', views.create_availability, name='create_availability'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('doctor-profile/', views.doctor_profile, name='doctor_profile'),
    path('patient-profile/', views.patient_profile, name='patient_profile'),
    path('api/doctor/<int:doctor_id>/slots/', views.doctor_availability_api, name='doctor_slots_api'),
]