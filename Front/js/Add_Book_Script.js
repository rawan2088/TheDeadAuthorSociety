document.addEventListener("DOMContentLoaded", async () => {
  const editBookId = sessionStorage.getItem("editBookId");
  const isEditMode = !!editBookId;

  // Input fields
  const nameInput = document.getElementById("name");
  const authInput = document.getElementById("auth");
  const catInput = document.getElementById("cat");
  const descInput = document.getElementById("desc");
  const heading = document.querySelector("h1");
  const submitBtn = document.querySelector("input[type='submit']");

  // If we are in Edit Mode, fetch the existing data
  if (isEditMode) {
    try {
      const response = await fetch(`${API}/books/${editBookId}/`, {
        credentials: "include", // Always include for auth-checked views
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const editBook = await response.json();
        nameInput.value = editBook.title;
        authInput.value = editBook.author;
        catInput.value = editBook.category;
        descInput.value = editBook.description;

        if (heading) heading.textContent = "Edit Book";
        if (submitBtn) submitBtn.value = "Save Changes";
      }
    } catch (err) {
      console.error("Error fetching book for edit:", err);
    }
  }

  // Handle Form
  document.querySelector("form").onsubmit = async function (e) {
    e.preventDefault();

    const payload = {
      title: nameInput.value.trim(),
      author: authInput.value.trim(),
      category: catInput.value.trim(),
      description: descInput.value.trim() || "No description provided.",
    };

    if (!payload.title || !payload.author || !payload.category) {
      alert("Please fill all required fields!");
      return;
    }

    let url = `${API}/books/`;
    let method = "POST";

    // If editing, change the URL to the specific book and use PUT
    if (isEditMode) {
      url = `${API}/books/${editBookId}/`;
      method = "PUT";
    } else {
      // If adding new, add default values that the model requires
      payload.published_date = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
      payload.totalCopies = 1;
      payload.availableCopies = 1;
    }

    try {
      const response = await fetch(url, {
        method: method,
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert(isEditMode ? "Book updated!" : "Book added!");
        sessionStorage.removeItem("editBookId"); // Clean up
        window.location.href = "Manage.html";
      } else {
        const errorData = await response.json();
        alert("Error: " + (errorData.error || "Failed to save book."));
      }
    } catch (err) {
      alert("Network error. Please try again.");
    }
  };
});
