// signup.js - Handles user registration logic

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signupForm");
  const errorMsg = document.getElementById("signupError");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const email = document.getElementById("email").value.trim();
    const role = document.querySelector('input[name="role"]:checked').value;

    // Clear previous error
    errorMsg.textContent = "";

    // Validation: check passwords match
    if (password !== confirmPassword) {
      errorMsg.textContent = "Passwords do not match.";
      return;
    }

    // Validation: check password length
    if (password.length < 6) {
      errorMsg.textContent = "Password must be at least 6 characters.";
      return;
    }

    // Validation: check username is not already taken
    const existingUser = getUserByUsername(username);
    if (existingUser) {
      errorMsg.textContent =
        "That username is already taken. Please choose another.";
      return;
    }

    // Build the new user object
    const users = getUsers();
    const ids = users.map((u) => u.id);
    const newId = users.length > 0 ? Math.max(...ids) + 1 : 1;

    const newUser = {
      id: newId,
      firstName,
      lastName,
      username,
      password,
      email,
      role,
    };

    // Save and redirect
    saveUser(newUser);
    alert("Account created successfully! Please log in.");
    window.location.href = "login.html";
  });
});
