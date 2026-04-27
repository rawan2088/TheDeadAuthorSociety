document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();

    if (!name || !email || !message) {
      showFeedback("Please fill in all fields.", "error");
      return;
    }

    if (!email.includes("@") || !email.includes(".")) {
      showFeedback("Please enter a valid email address.", "error");
      return;
    }

    if (message.length < 10) {
      showFeedback(
        "Your message is a bit short — please add more detail.",
        "error",
      );
      return;
    }

    // Success
    showFeedback(
      "Your message has been sent! We'll get back to you soon.",
      "success",
    );
    form.reset();
  });

  function showFeedback(text, type) {
    const old = document.getElementById("contactFeedback");
    if (old) old.remove();

    const div = document.createElement("div");
    div.id = "contactFeedback";
    div.className = `alert alert-${type === "error" ? "error" : "success"}`;
    div.textContent = text;

    form.insertAdjacentElement("beforebegin", div);

    // Auto-remove after 5 seconds
    setTimeout(() => div.remove(), 5000);
  }
});
