// Signup.js - updated for Django backend
document.addEventListener("DOMContentLoaded", function () {
  const form     = document.getElementById("signupForm");
  const errorMsg = document.getElementById("signupError");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    errorMsg.textContent = "";

    const firstName      = document.getElementById("first-name").value.trim();
    const lastName       = document.getElementById("last-name").value.trim();
    const username       = document.getElementById("username").value.trim();
    const password       = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const email          = document.getElementById("email").value.trim();
    const role           = document.querySelector('input[name="role"]:checked').value;

    // Client-side check first (fast feedback)
    if (password !== confirmPassword) {
      errorMsg.textContent = "Passwords do not match.";
      return;
    }
    if (password.length < 6) {
      errorMsg.textContent = "Password must be at least 6 characters.";
      return;
    }

    // If admin is selected, ask for the secret code
    let adminCode = "";
    if (role === "admin") {
      adminCode = prompt("Enter the admin secret code:");
      if (!adminCode) return;
    }

    try {
      const response = await fetch("/api/signup/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firstName,
          lastName,
          username,
          password,
          confirmPassword,
          email,
          role,
          adminCode,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Server returned an error (400, 403, etc.)
        errorMsg.textContent = data.error;
        return;
      }

      alert("Account created successfully! Please log in.");
      window.location.href = "login.html";

    } catch (err) {
      errorMsg.textContent = "Something went wrong. Please try again.";
      console.error(err);
    }
  });
});