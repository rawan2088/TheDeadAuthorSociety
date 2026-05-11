document.addEventListener("DOMContentLoaded", async () => {
  const editBookId = sessionStorage.getItem("editBookId");
  const isEditMode = !!editBookId;
  const numInput = document.getElementById("num");
  const nameInput = document.getElementById("name");
  const authInput = document.getElementById("auth");
  const catInput = document.getElementById("cat");
  const descInput = document.getElementById("desc");
  const heading = document.querySelector("h1");
  const submitBtn = document.querySelector("input[type='submit']");
  const API = "http://127.0.0.1:8000/api";

  // reserved until we edit
  let editBook = null;
  if (isEditMode) {
    const response = await fetch(`${API}/books/${editBookId}/`, {
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    editBook = await response.json();

    numInput.value = editBook.id;
    nameInput.value = editBook.title;
    authInput.value = editBook.author;
    catInput.value = editBook.category;
    descInput.value = editBook.description;

    numInput.disabled = true;
    if (heading) heading.textContent = "Edit Book";
    if (submitBtn) submitBtn.value = "Save Changes";
  } else {
    numInput.disabled = true;
  }

  document.querySelector("form").onsubmit = async function (e) {
    e.preventDefault();

    const bookName = nameInput.value.trim();
    const author = authInput.value.trim();
    const category = catInput.value.trim();
    const desc = descInput.value.trim();

    if (!bookName || !author || !category) {
      alert("Please fill all required fields before saving!");
      return;
    }

    if (isEditMode) {
      await fetch(`${API}/books/${editBookId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          title: bookName,
          author: author,
          category: category,
          description: desc,
        }),
      });

      sessionStorage.removeItem("editBookId");
      alert(`"${bookName}" has been updated successfully!`);
      window.location.href = "Manage.html";
    } else {
      await fetch(`${API}/books/`, {
        method: "POST",
        headers: {
          // tells Django we are sending JSON
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          title: bookName,
          author: author,
          category: category,
          description: desc || "No description provided.",
          published_date: new Date().getFullYear() + "-01-01",
          image: "",
          totalCopies: 1,
          availableCopies: 1,
        }),
      });

      alert(`"${bookName}" has been added successfully!`);
      document.querySelector("form").reset();
    }
  };
});
