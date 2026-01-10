from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from rest_framework import viewsets
from .models import ParkingZone, ParkingSpot, Reservation
from .forms import ReservationForm
from .serializers import ParkingSpotSerializer, ReservationSerializer

# --- WIDOKI CORE & DATA ---

def home(request):
    zones = ParkingZone.objects.all()
    return render(request, 'parking/home.html', {'zones': zones})

def zone_detail(request, zone_id):
    zone = get_object_or_404(ParkingZone, pk=zone_id)
    return render(request, 'parking/zone_detail.html', {'zone': zone})

@login_required
def reservation_list(request):
    # Wymóg: Lista danych + dostęp tylko dla zalogowanych
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'parking/reservation_list.html', {'reservations': reservations})

@login_required
def create_reservation(request):
    # Wymóg: Zapis danych przez formularz
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Rezerwacja udana!")
            return redirect('reservation_list')
        else:
            messages.error(request, "Popraw błędy w formularzu.")
    else:
        form = ReservationForm()
    return render(request, 'parking/reservation_form.html', {'form': form, 'title': 'Nowa Rezerwacja'})

@login_required
def edit_reservation(request, pk):
    # Wymóg: Edycja danych
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'parking/reservation_form.html', {'form': form, 'title': 'Edytuj Rezerwację'})

# --- WIDOKI UŻYTKOWNIKA ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto utworzone. Zaloguj się.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- REST API ---
# Wymóg: 2 endpointy JSON

class ParkingSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer