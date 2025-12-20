from django.contrib import admin
from .models import Availability, Booking

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked', 'date', 'doctor')
    search_fields = ('doctor__username',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'get_doctor', 'get_date', 'get_time', 'booked_at')
    list_filter = ('booked_at', 'availability__date')
    search_fields = ('patient__username', 'availability__doctor__username')
    
    def get_doctor(self, obj):
        return obj.availability.doctor.username
    get_doctor.short_description = 'Doctor'
    
    def get_date(self, obj):
        return obj.availability.date
    get_date.short_description = 'Date'
    
    def get_time(self, obj):
        return f"{obj.availability.start_time} - {obj.availability.end_time}"
    get_time.short_description = 'Time'