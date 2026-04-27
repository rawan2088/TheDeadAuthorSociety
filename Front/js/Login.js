// login.js - Handles user login logic

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const errorMsg = document.getElementById("loginError");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    // Clear previous error
    errorMsg.textContent = "";

    // Look up user by username
    const user = getUserByUsername(username);

    if (!user) {
      errorMsg.textContent = "No account found with that username.";
      return;
    }

    if (user.password !== password) {
      errorMsg.textContent = "Incorrect password. Please try again.";
      return;
    }

    // Login successful
    setCurrentUser(user);

    // Redirect to home page
    window.location.href = "index.html";
  });
});
