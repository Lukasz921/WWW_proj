// Walidacja formularza rezerwacji
function validateReservationForm() {
    // Pobieramy elementy formularza po ID (Django generuje id_nazwapola)
    const startTimeInput = document.getElementById('id_start_time');
    const endTimeInput = document.getElementById('id_end_time');
    const plateInput = document.getElementById('id_license_plate');

    // Jeśli nie ma tych pól na stronie (np. inny formularz), przerywamy
    if (!startTimeInput || !endTimeInput || !plateInput) return true;

    const start = new Date(startTimeInput.value);
    const end = new Date(endTimeInput.value);
    const plate = plateInput.value.trim();
    const now = new Date();

    let isValid = true;
    let errorMessage = "";

    // 1. Sprawdzenie czy data końcowa jest po początkowej
    if (start >= end) {
        errorMessage += "- Data końcowa musi być późniejsza niż początkowa.\n";
        isValid = false;
    }

    // 2. Sprawdzenie czy rezerwacja nie jest w przeszłości
    if (start < now) {
        errorMessage += "- Nie można rezerwować terminu w przeszłości.\n";
        isValid = false;
    }

    // 3. Sprawdzenie długości tablicy
    if (plate.length < 3) {
        errorMessage += "- Numer rejestracyjny jest za krótki (min. 3 znaki).\n";
        isValid = false;
    }

    if (!isValid) {
        alert("Błąd walidacji:\n" + errorMessage);
    }

    return isValid;
}

// Dodatkowa funkcjonalność JS (Wymóg sekcji Website - coś więcej niż walidacja)
document.addEventListener("DOMContentLoaded", function() {
    console.log("Parking System Loaded");

    // Przykład: Podświetlenie aktywnego linku w menu
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav .links a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.borderBottom = "2px solid #3498db";
        }
    });
});