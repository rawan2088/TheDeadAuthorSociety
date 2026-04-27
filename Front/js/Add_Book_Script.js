document.addEventListener("DOMContentLoaded", () => {
  const editBook = JSON.parse(sessionStorage.getItem("editBook"));
  const isEditMode = !!editBook;

  const numInput = document.getElementById("num");
  const nameInput = document.getElementById("name");
  const authInput = document.getElementById("auth");
  const catInput = document.getElementById("cat");
  const descInput = document.getElementById("desc");
  const heading = document.querySelector("h1");
  const submitBtn = document.querySelector("input[type='submit']");

  if (isEditMode) {
    numInput.value = editBook.id;
    nameInput.value = editBook.title;
    authInput.value = editBook.author;
    catInput.value = editBook.category;
    descInput.value = editBook.description;

    numInput.disabled = true;
    if (heading) heading.textContent = "Edit Book";
    if (submitBtn) submitBtn.value = "Save Changes";
  } else {
    const books = getBooks();
    const nextId =
      books.length > 0 ? Math.max(...books.map((b) => b.id)) + 1 : 1;
    numInput.value = nextId;
    numInput.disabled = true;
  }

  document.querySelector("form").onsubmit = function (e) {
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
      const updatedBook = {
        ...editBook,
        title: bookName,
        author: author,
        category: category,
        description: desc || editBook.description,
      };
      updateBook(updatedBook);
      sessionStorage.removeItem("editBook");
      alert(`"${bookName}" has been updated successfully!`);
      window.location.href = "Manage.html";
    } else {
      const books = getBooks();
      const nextId =
        books.length > 0 ? Math.max(...books.map((b) => b.id)) + 1 : 1;

      const newBook = {
        id: nextId,
        title: bookName,
        author: author,
        published: new Date().getFullYear(),
        category: category,
        description: desc || "No description provided.",
        image: "../Assets/default.jpg",
        totalCopies: 1,
        availableCopies: 1,
      };

      saveBook(newBook);
      alert(`"${bookName}" has been added successfully!`);
      document.querySelector("form").reset();

      const newNext = nextId + 1;
      numInput.value = newNext;
    }
  };
});
