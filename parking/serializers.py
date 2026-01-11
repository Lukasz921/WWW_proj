from rest_framework import serializers
from .models import ParkingSpot, Reservation

class ParkingSpotSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    class Meta:
        model = ParkingSpot
        fields = ['id', 'spot_number', 'zone_name', 'is_disabled_friendly']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'license_plate', 'start_time', 'end_time']

# Serializacja pod wygodę np. aplikacje mobilne nie rozumieją obiektów pythona, ale rozumieją JSON
# Dla klasy ParkingSpotSerializer zone_name jest fk (kluczem obcym)
# Gdybyśmy zrobili inaczej niż w lini 5, to JSON by miał np. "zone": 5, a aplkiacja mobilna nie jak to interpretować
# Stąd source='zone.name' i wówczas w jsonie np. "zone" = "Poziom A"