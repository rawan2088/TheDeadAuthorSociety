document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const errorMsg = document.getElementById("loginError");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    errorMsg.textContent = "";

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    try {
      const response = await fetch(`${API}/login/`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        errorMsg.textContent = data.error;
        return;
      }

      // Save user info to sessionStorage so navbar still works
      sessionStorage.setItem("currentUser", JSON.stringify(data.user));

      window.location.href = "index.html";
    } catch (err) {
      errorMsg.textContent = "Something went wrong. Please try again.";
      console.error(err);
    }
  });
});
