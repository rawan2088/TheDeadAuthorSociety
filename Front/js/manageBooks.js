let booksContainer = document.getElementById("bookContainer");
const API = "http://127.0.0.1:8000/api";

async function handleDelete(id) {
  if (confirm("Are you sure you want to delete this book?")) {
    await fetch(`${API}/books/${id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    renderBooks();
  }
}

async function handleAddCopy(id) {
  await fetch(`${API}/books/${id}/add-copy/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });
  renderBooks();
}

function handleEdit(id) {
  sessionStorage.setItem("editBook", id);
  window.location.href = "Add_Book.html";
}

async function renderBooks() {
  booksContainer.innerHTML = "";

  const response = await fetch("${API}/books/", {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });
  const books = await response.json();

  books.forEach((book) => {
    // it is better to make an invisible anchor over the div card element
    // since it is not valid html to put interactive elements inside an anchor tag

    const bookCard = document.createElement("div");
    // bookCard.href = `./book${book.id}.html`;

    bookCard.classList.add("bookCard");
    bookCard.innerHTML = `
        <a href="./book.html?id=${book.id}"></a>
          <img
            src="${book.image}"
            height="200"
            width="150"
            alt="${book.title}"
          />
          <h3>${book.title}</h3>
          <p><strong>Author:</strong> ${book.author}</p>
          <p><strong>Published:</strong> ${book.published_date}</p>
          <p><strong>Category:</strong> ${book.category}</p>
          <p>
             ${book.description}
          </p>
          <!-- would only be a true or false statement depending on the number in stock -->
          <p><strong>Availability:</strong> ${book.availableCopies > 0 ? "In Stock" : "Out of Stock"}</p>
          <div class="card-actions">
            <button class="btn btn-primary add-copy-btn">+ Copy</button>
            <button class="btn btn-secondary edit-btn">Edit</button>
            <button class="btn btn-danger delete-btn">Delete</button>
          </div>
    `;

    const invisible = document.createElement("a");
    invisible.classList.add("invisible-link");
    invisible.href = `book.html?id=${book.id}`;
    bookCard.appendChild(invisible);

    bookCard.querySelectorAll(".card-actions button").forEach((btn) => {
      btn.addEventListener("click", (e) => e.stopPropagation());
    });

    bookCard
      .querySelector(".add-copy-btn")
      .addEventListener("click", () => handleAddCopy(book.id));
    bookCard
      .querySelector(".edit-btn")
      .addEventListener("click", () => handleEdit(book.id));
    bookCard
      .querySelector(".delete-btn")
      .addEventListener("click", () => handleDelete(book.id));
    booksContainer.appendChild(bookCard);
  });
}
// would save the current book in the session storage,
// then check inside the add book page if there is data, if there is then it would be an edit, if not then it would be an add

renderBooks();
