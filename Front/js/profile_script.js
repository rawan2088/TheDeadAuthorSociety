document.addEventListener("DOMContentLoaded", () => {
  const user = getCurrentUser();

  if (!user) {
    window.location.href = "login.html";
    return;
  }

  const roleEl = document.getElementById("displayRole");
  const usernameEl = document.getElementById("displayUsername");
  const emailEl = document.getElementById("displayEmail");

  if (roleEl) roleEl.textContent = user.role;
  if (usernameEl) usernameEl.textContent = user.username;
  if (emailEl) emailEl.textContent = user.email || "—";

  // Form submit
  document.querySelector("form").onsubmit = function (e) {
    e.preventDefault();

    const newUsername = document.getElementById("user").value.trim();
    const newEmail = document.getElementById("email").value.trim();
    const currentPass = document.getElementById("Cpass").value.trim();
    const newPass = document.getElementById("pass").value.trim();

    if (!newUsername && !newEmail && !currentPass && !newPass) {
      alert("Please fill at least one field to make changes!");
      return;
    }

    if (newEmail && !newEmail.includes("@")) {
      alert("Invalid email address!");
      return;
    }

    if (currentPass && !newPass) {
      alert("You must enter a new password to change it!");
      return;
    }
    if (newPass && !currentPass) {
      alert("You must enter your current password to change it!");
      return;
    }
    if (currentPass && currentPass !== user.password) {
      alert("Current password is incorrect!");
      return;
    }
    if (newPass && newPass.length < 6) {
      alert("New password must be at least 6 characters.");
      return;
    }

    const updatedUser = { ...user };

    if (newUsername) updatedUser.username = newUsername;
    if (newEmail) updatedUser.email = newEmail;
    if (newPass) updatedUser.password = newPass;

    updateUser(updatedUser);
    setCurrentUser(updatedUser);

    alert("Changes saved successfully!");

    if (usernameEl) usernameEl.textContent = updatedUser.username;
    if (emailEl) emailEl.textContent = updatedUser.email || "—";

    document.querySelector("form").reset();
  };
});
