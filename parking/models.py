from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

# Plik bazy danych

# Model 1: Strefa parkingu
# Tabela w bazie z 2 kolumnami - name(str) oraz price_per_hour(decimal)
class ParkingZone(models.Model):
    name = models.CharField(max_length=50, verbose_name="Zone name")
    price_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Price per hour",
        validators=[MinValueValidator(0.00)] # blokuje ujemne liczby
    )
    def __str__(self):
        return f"{self.name} ({self.price_per_hour} $/h)"

# Model 2: Miejsce parkingowe z relacją do modelu strefy (klucz obcy)
# Każde miejsce parkingowe ma przydzieloną strefę (1:N - jedna strefa, wiele miejsc)
# Tabela w bazie z 3 kolumnami - fk na zone, spot_numer(str) oraz is_disabled_friendly(bool)
class ParkingSpot(models.Model):
    zone = models.ForeignKey(ParkingZone, on_delete=models.CASCADE, related_name='spots')
    spot_number = models.CharField(max_length=10, verbose_name="Spot number")
    is_disabled_friendly = models.BooleanField(default=False, verbose_name="For disabled")
    def __str__(self):
        return f"Spot {self.spot_number} ({self.zone.name})"

# Model 3: Rezerwacja z relacja do modelu usera i miejsca parkingowego
# Tabela w bazie z 6 kolumnami - fk na usera, fk na parking spot,
# license_plate(str), start_time(date), end_time(date), created_at(date)
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, verbose_name="Spot")
    license_plate = models.CharField(max_length=20, verbose_name="License")
    start_time = models.DateTimeField(verbose_name="Start time")
    end_time = models.DateTimeField(verbose_name="End time")
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if not self.start_time or not self.end_time:
            return
        if self.start_time >= self.end_time:
            raise ValidationError("Start time has to be earlier than end time.")
        if self.start_time < timezone.now():
            raise ValidationError("Cannon reserve in past.")
        # Walidacja - jeżeli oba obiekty istnieją (aby nie porównywać none) to sprawdzamy czy daty są poprawne

        collisions = Reservation.objects.filter( # pobieramy wszystkie rezerwacje na to miejsce
            spot=self.spot,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        # wykluczamy samego siebie z tej listy (przy edycji!)
        if self.pk:
            collisions = collisions.exclude(pk=self.pk)
        if collisions.exists():
            raise ValidationError(
                f"This spot is already taken. Reservation ID: {collisions.first().id}")

    def __str__(self):
        return f"Reservation: {self.license_plate} ({self.start_time})"