document.addEventListener("DOMContentLoaded", function () {
    const passwordField = document.getElementById("passwordfield");
    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword) { // Ensure the element exists before adding an event listener
        togglePassword.addEventListener("click", function () {
            if (passwordField.type === "password") {
                passwordField.type = "text";
                togglePassword.textContent = "Hide";
            } else {
                passwordField.type = "password";
                togglePassword.textContent = "Show";
            }
        });
    }
});
