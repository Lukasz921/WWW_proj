from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Model 1: Strefa Parkingu (np. Poziom A, VIP)
class ParkingZone(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nazwa strefy")
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena za godzinę")

    def __str__(self):
        return f"{self.name} ({self.price_per_hour} PLN/h)"


# Model 2: Miejsce Parkingowe (Relacja do Strefy)
class ParkingSpot(models.Model):
    zone = models.ForeignKey(ParkingZone, on_delete=models.CASCADE, related_name='spots')
    spot_number = models.CharField(max_length=10, verbose_name="Numer miejsca")
    is_disabled_friendly = models.BooleanField(default=False, verbose_name="Dla niepełnosprawnych")

    def __str__(self):
        return f"Miejsce {self.spot_number} ({self.zone.name})"


# Model 3: Rezerwacja (Relacja do Usera i Miejsca)
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, verbose_name="Miejsce")
    license_plate = models.CharField(max_length=20, verbose_name="Rejestracja")
    start_time = models.DateTimeField(verbose_name="Początek")
    end_time = models.DateTimeField(verbose_name="Koniec")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Wymóg: Walidacja po stronie serwera
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Data końcowa musi być późniejsza niż początkowa.")

    def __str__(self):
        return f"Rezerwacja: {self.license_plate} ({self.start_time})"