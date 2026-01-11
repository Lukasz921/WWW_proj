// Walidacja forma rezerwacji
function validateReservationForm() {
    // Pobieramy elementy forma po ID (Django generuje id_nazwapola)
    const startTimeInput = document.getElementById('id_start_time');
    const endTimeInput = document.getElementById('id_end_time');
    const plateInput = document.getElementById('id_license_plate');
    // Walidacja, czy elementy są, czy to może inny form
    if (!startTimeInput || !endTimeInput || !plateInput) return true;

    const start = new Date(startTimeInput.value);
    const end = new Date(endTimeInput.value);
    const plate = plateInput.value.trim();
    const now = new Date();

    let isValid = true;
    let errorMessage = "";
    if (start >= end) {
        errorMessage += "- Start time has to be earlier than end time.\n";
        isValid = false;
    }
    if (start < now) {
        errorMessage += "- Cannon reserve in past.\n";
        isValid = false;
    }
    if (plate.length < 3) {
        errorMessage += "- License plate number is too short.\n";
        isValid = false;
    }
    if (!isValid) {
        alert("Validation error:\n" + errorMessage);
    }
    return isValid;
}

// Dodatkowa funkcjonalność JS
document.addEventListener("DOMContentLoaded", function() {
    console.log("Parking System Loaded");
    // Podświetlenie aktywnego linku w menu
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav .links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.borderBottom = "2px solid #3498db";
        }
    });
});