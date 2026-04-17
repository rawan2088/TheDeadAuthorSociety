const borrowedContainer = document.getElementById("bookContainer");

function handleReturn(bookId) {
  if (confirm("Are you sure you want to return this book?")) {
    returnBook(bookId);
    renderBorrowedBooks();
  }
}

function renderBorrowedBooks() {
  const user = getCurrentUser();

  if (!user) {
    borrowedContainer.innerHTML = "<p>Please log in to view your books.</p>";
    return;
  }

  const borrowRecords = getBorrowedByUser(user);
  const allBooks = getBooks();

  borrowedContainer.innerHTML = "";

  if (borrowRecords.length === 0) {
    borrowedContainer.innerHTML =
      "<p>You have no borrowed books at the moment.</p>";
    return;
  }

  borrowRecords.forEach((record) => {
    // Look up the full book object using the bookId from the borrow record
    const book = allBooks.find((b) => b.id === record.bookId);

    if (!book) return; // skip if book was deleted

    const bookCard = document.createElement("div");
    bookCard.classList.add("bookCard");

    bookCard.innerHTML = `
      <img
        src="${book.image}"
        height="200"
        width="150"
        alt="${book.title}"
      />
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Borrowed On:</strong> ${record.borrowDate || "N/A"}</p>
      <div class="card-actions">
        <button class="btn btn-primary return-btn">Return Book</button>
      </div>
    `;

    // Invisible link to book details
    const invisible = document.createElement("a");
    invisible.classList.add("invisible-link");
    invisible.href = `book.html?id=${book.id}`;
    bookCard.appendChild(invisible);

    // Return button — stop propagation so the invisible link doesn't fire
    const returnBtn = bookCard.querySelector(".return-btn");
    returnBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      handleReturn(record.id);
    });

    borrowedContainer.appendChild(bookCard);
  });
}

document.addEventListener("DOMContentLoaded", renderBorrowedBooks);
