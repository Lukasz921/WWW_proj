from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Tworzymy form na podstawie modelu Rejestracji - automatycznie tworzony jest formularz
# Fields to elementy, które użytkownik wpisuje sam, reszta tzn user i created_at jest automatycznie wypełniane
# Widgets odpowiada za połączenie forma z plikami HTML i CSS
# Dla spota dodajemy klasę CSS do pola HTML (form-control to klasa na podstawie której generowany jest wygląd)
# Dla license_plate analog + dodajemy podpowiedź jak przykładowo ma wyglądać rejestracja (placeholder)
# Dla start_time i end_time to samo + datetime-local automatycznie wygeneruje kalendarz html-owy na stronie

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['spot', 'license_plate', 'start_time', 'end_time']
        widgets = {
            'spot': forms.Select(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. WA 12345'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    def clean_license_plate(self):
        plate = self.cleaned_data.get('license_plate')
        if len(plate) < 3:
            raise forms.ValidationError("License plate number is too short.")
        return plate

# Funkcja clean_license_plate jest uruchamiana automatycznie przy walidacji forma
# To zapobiega takiemu oszustwu, że ktoś w przeglądarce sobie js podmieni to i tak to jest walidowane tutaj
# Jeśli jest okej, to tworzona jest rezerwacja i wysyłana do bazy

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")
    class Meta:
        model = User
        fields = ("username", "email")
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email