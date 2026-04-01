let booksContainer = document.getElementById("bookContainer");

function handleDelete(id) {
  if (confirm("Are you sure you want to delete this book?")) {
    deleteBook(id);
    renderBooks();
  }
}

function renderBooks() {
  booksContainer.innerHTML = "";

  const books = getBooks();

  books.forEach((book) => {
    // it is better to make an invisible anchor over the div card element
    // since it is not valid html to put interactive elements inside an anchor tag

    const bookCard = document.createElement("div");
    // bookCard.href = `./book${book.id}.html`;

    bookCard.classList.add("bookCard");
    bookCard.innerHTML = `
        <a href="./book${book.id}.html"></a>
          <img
            src="${book.image}"
            height="200"
            width="150"
            alt="${book.title}"
          />
          <h3>${book.title}</h3>
          <p><strong>Author:</strong> ${book.author}</p>
          <p><strong>Published:</strong> ${book.published}</p>
          <p><strong>Category:</strong> ${book.category}</p>
          <p>
             ${book.description}
          </p>
          <!-- would only be a true or false statement depending on the number in stock -->
          <p><strong>Availability:</strong> ${book.availableCopies > 0 ? "In Stock" : "Out of Stock"}</p>
          <div class="card-actions">
            <button class="btn btn-primary">+</button>
            <button class="btn btn-secondary">Edit</button>
            <button class="btn btn-danger" onclick="handleDelete(${book.id})">Delete</button>
          </div>
    `;

    const invisible = document.createElement("a");
    invisible.classList.add("invisible-link");
    invisible.href = `book${book.id}.html`;
    bookCard.appendChild(invisible);

    bookCard.querySelectorAll(".card-actions button").forEach((btn) => {
      btn.addEventListener("click", (e) => e.stopPropagation());
    });

    bookCard.querySelector(".btn-danger").addEventListener("click", () => {
      handleDelete(book.id);
    });

    booksContainer.appendChild(bookCard);
  });
}
//   would save the current book in the session storage,
// then check inside the add book page if there is data, if there is then it would be an edit, if not then it would be an add

renderBooks();
