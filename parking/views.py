from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import ParkingZone, ParkingSpot, Reservation
from .forms import ReservationForm, CustomUserCreationForm
from .serializers import ParkingSpotSerializer, ReservationSerializer

# Strona główna
# Bierze wszystkie strefy parkingowe i je wyświetla
# Pokazuje, który plik hmtl wyświetlić i wkleja tam zones
def home(request):
    zones = ParkingZone.objects.all()
    return render(request, 'parking/home.html', {'zones': zones})

# Szczegóły strefy, analog do powyższego
# Dodatkowo walidacja - jeśli użytkownik wpisze strefę, która nie istnieje to 404 page not found
# Trochę jak unwrap_or_else w Rust
def zone_detail(request, zone_id):
    zone = get_object_or_404(ParkingZone, pk=zone_id)
    return render(request, 'parking/zone_detail.html', {'zone': zone})

# Lista rezerwacji - wymagane zalogowanie
# Bierze rezerwacje tego usera, sortuje po created_at
# Do htmla i wkleja reservations
@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'parking/reservation_list.html', {'reservations': reservations})

# Tworzenie rezerwacji - wymagane zalogowanie
# POST - formularz już stworzony, użytkownik chce go zapisać
# GET - użytkownik woła stworzenie formularza
@login_required
def create_reservation(request):
    if request.method == 'POST': # użytkownik kliknął zapisz - metoda POST - chcemy umieścić rekord w bazie danych
        form = ReservationForm(request.POST) # tworzymy reservation form z pliku forms.py (klasę form już wypełnioną)
        if form.is_valid(): # walidacja - np. metoda clean_license_plate + daty czy dobre (już w modelu)
            reservation = form.save(commit=False) # zapisujemy forma, ale w bazie jeszcze nie ma
            reservation.user = request.user # wskazujemy kto robi rezerwację
            reservation.save() # zapis do bazy
            messages.success(request, "Reservation successfully created.!")
            return redirect('reservation_list')
        else:
            messages.error(request, "Correct errors in form.")
    else: # użytkownik dopiero wszedł na stronę i chce pusty formularz - metoda GET
        form = ReservationForm()
    return render(request, 'parking/reservation_form.html', {'form': form, 'title': 'New Reservation'})

# Edycja rezerwacji - wymagane zalogowanie
@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':  # użytkownik kliknął zapisz - metoda POST - chcemy zmodyfikować rekord w bazie danych
        form = ReservationForm(request.POST, instance=reservation) # formularz ma obecne dane z bazy (modyfikowalne)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation) # formularz ma obecne dane z bazy (modyfikowalne)
    return render(request, 'parking/reservation_form.html', {'form': form, 'title': 'Edit Reservation'})

# Rejestracja użytkownika
# Tutaj dotyczy to domyślnego modelu user Django
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # is_valid() automatycznie sprawdza:
            # 1. Unikalność loginu w bazie
            # 2. Zgodność obu haseł
            # 3. Siłę hasła (wg zasad z settings.py)
            form.save()
            messages.success(request, "Account created. Log in!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Automatycznie tworzą stronę pod adresem /api/spots/, która zwraca JSON z listą miejsc (readonly, aby nie móc zmienić)
class ParkingSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer