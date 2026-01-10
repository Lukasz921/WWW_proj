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