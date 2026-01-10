from django.contrib import admin
from .models import ParkingZone, ParkingSpot, Reservation

admin.site.register(ParkingZone)
admin.site.register(ParkingSpot)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'spot', 'user', 'start_time', 'end_time')
    list_filter = ('spot__zone', 'start_time')