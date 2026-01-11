from django.contrib import admin
from .models import ParkingZone, ParkingSpot, Reservation

# Dla Parking Zone to co dla Parking Spot bez filtra
@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_hour')
    ordering = ('price_per_hour',)

# Dla Parking Spot to samo co dla Reservation
# Dodatkowo bazowe sortowanie najpierw po strefie, a potem po numerze miejsca
@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('spot_number', 'zone', 'is_disabled_friendly')
    list_filter = ('zone', 'is_disabled_friendly')
    ordering = ('zone', 'spot_number')

# Dla Reservation przeciążamy metodę wyświetlania
# Zamiast domyślnych ustawień z metodami __str__ tworzymy tabelę z kolumnami license_plate, spot itd.
# Dodatkowo prosta filtracja z boku tabelki po strefie / po czasie startu rezerwacji
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'spot', 'user', 'start_time', 'end_time')
    list_filter = ('spot__zone', 'start_time')

# te przeciążone metody nie korzystają z funkcji __str__ zdefiniowanych w modelach