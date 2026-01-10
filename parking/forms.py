from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['spot', 'license_plate', 'start_time', 'end_time']
        widgets = {
            # 1. Typ: Select (z modelu)
            'spot': forms.Select(attrs={'class': 'form-control'}),
            # 2. Typ: TextInput
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. WA 12345'}),
            # 3. Typ: DateTime-Local (HTML5)
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # 4. Typ: DateTime-Local
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean_license_plate(self):
        # Dodatkowa walidacja serwerowa
        plate = self.cleaned_data.get('license_plate')
        if len(plate) < 3:
            raise forms.ValidationError("Numer rejestracyjny jest za krótki.")
        return plate