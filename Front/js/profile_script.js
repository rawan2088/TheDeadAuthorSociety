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
  document.querySelector("form").onsubmit = async function (e) {
    e.preventDefault();

    const newUsername = document.getElementById("user").value.trim();
    const newEmail = document.getElementById("email").value.trim();
    const newPass = document.getElementById("pass").value.trim();
    const currentPass = document.getElementById("Cpass").value.trim();

    if (!newUsername && !newEmail && !newPass) {
      alert("Please fill at least one field to make changes!");
      return;
    }

    if (newEmail && !newEmail.includes("@")) {
      alert("Invalid email address!");
      return;
    }

    if (newPass && !currentPass) {
      alert("You must enter your current password to change it!");
      return;
    }

    if (newPass && newPass.length < 6) {
      alert("New password must be at least 6 characters.");
      return;
    }

    try {
      const res = await fetch(`${API}/me/update/`, {
        method: "PUT",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          username: newUsername || undefined,
          email: newEmail || undefined,
          currentPassword: currentPass || undefined,
          newPassword: newPass || undefined,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Something went wrong.");
        return;
      }

      // Update sessionStorage so the navbar reflect
      sessionStorage.setItem("currentUser", JSON.stringify(data.user));

      alert("Changes saved successfully!");
      document.querySelector("form").reset();

      // Refresh displayed info
      if (usernameEl) usernameEl.textContent = data.user.username;
      if (emailEl) emailEl.textContent = data.user.email || "—";
    } catch (err) {
      alert("Network error. Please try again.");
      console.error(err);
    }
  };
});
