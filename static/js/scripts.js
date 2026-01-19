document.addEventListener("DOMContentLoaded", function() {
    console.log("Parking System Loaded");
    highlightActiveLink();
    setupLoginFormValidation();
});
function validateReservationForm() {
    const startTimeInput = document.getElementById('id_start_time');
    const endTimeInput = document.getElementById('id_end_time');
    const plateInput = document.getElementById('id_license_plate');
    if (!startTimeInput || !endTimeInput || !plateInput) return true;
    startTimeInput.style.border = "";
    endTimeInput.style.border = "";
    plateInput.style.border = "";
    const start = new Date(startTimeInput.value);
    const end = new Date(endTimeInput.value);
    const plate = plateInput.value.trim();
    const now = new Date();
    let isValid = true;
    let errorMessages = [];
    if (start >= end) {
        errorMessages.push("- Start time cannot be bigger than end time");
        startTimeInput.style.border = "2px solid red";
        endTimeInput.style.border = "2px solid red";
        isValid = false;
    }
    if (start < now) {
        errorMessages.push("- Cannot reserve in the past");
        startTimeInput.style.border = "2px solid red";
        isValid = false;
    }
    if (plate.length < 3) {
        errorMessages.push("- License plate too short (min. 3).");
        plateInput.style.border = "2px solid red";
        isValid = false;
    }
    if (!isValid) {
        alert("Validation error:\n" + errorMessages.join("\n"));
    }
    return isValid;
}
function setupLoginFormValidation() {
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');
    if (usernameInput && passwordInput) {
        const form = usernameInput.closest('form');
        if (form) {
            form.addEventListener('submit', function(event) {
                let hasError = false;
                let errors = [];
                usernameInput.style.borderColor = "#ccc";
                passwordInput.style.borderColor = "#ccc";
                if (usernameInput.value.trim() === "") {
                    errors.push("Please, write username");
                    usernameInput.style.borderColor = "#e74c3c";
                    hasError = true;
                }
                if (passwordInput.value.trim() === "") {
                    errors.push("Please, write password");
                    passwordInput.style.borderColor = "#e74c3c";
                    hasError = true;
                }
                if (hasError) {
                    event.preventDefault();
                    alert("Login form:\n" + errors.join("\n"));
                }
            });
        }
    }
}
function highlightActiveLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav .links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.borderBottom = "2px solid #3498db";
            link.style.fontWeight = "bold";
        }
    });
}