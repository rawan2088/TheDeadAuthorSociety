<<<<<<< HEAD

const borrowedContainer = document.getElementById("bookContainer");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
}

async function handleReturn(borrowId, card) {
  if (!confirm("Are you sure you want to return this book?")) return;

  try {
    const res = await fetch(`${API}/borrowed/${borrowId}/return/`, {
      method:      "POST",
      credentials: "include",
      headers:     { "X-CSRFToken": getCookie("csrftoken") },
    });
    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "Could not return the book.");
      return;
    }

    // Remove the card from the DOM immediately
    card.remove();

    // If no cards left, show empty message
    if (!borrowedContainer.querySelector(".bookCard")) {
      borrowedContainer.innerHTML = "<p>You have no borrowed books at the moment.</p>";
    }
  } catch (err) {
    console.error(err);
    alert("Network error. Please try again.");
  }
}

function renderRecords(records) {
  borrowedContainer.innerHTML = "";

  if (!records || records.length === 0) {
    borrowedContainer.innerHTML = "<p>You have no borrowed books at the moment.</p>";
    return;
  }

  records.forEach((record) => {
    
    const book    = record.book;
    const bookCard = document.createElement("div");
    bookCard.classList.add("bookCard");

    bookCard.innerHTML = `
      <img
        src="${book.image || "../Assets/default.jpg"}"
        height="200"
        width="150"
        alt="${book.title}"
      />
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Borrowed On:</strong> ${record.borrowDate || "N/A"}</p>
      ${record.returnDate ? `<p><strong>Returned On:</strong> ${record.returnDate}</p>` : ""}
      <div class="card-actions">
        <button class="btn btn-primary return-btn">Return Book</button>
      </div>
    `;

    // Invisible link to book details
    const invisibleLink    = document.createElement("a");
    invisibleLink.classList.add("invisible-link");
    invisibleLink.href     = `book.html?id=${book.id}`;
    bookCard.appendChild(invisibleLink);

    // Return button — stop propagation so the invisible link doesn't fire
    const returnBtn = bookCard.querySelector(".return-btn");
    returnBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      handleReturn(record.borrowId, bookCard);
    });

    borrowedContainer.appendChild(bookCard);
  });
}


document.addEventListener("DOMContentLoaded", async () => {
  // Quick check: is there a logged-in user in session storage?
  const user = getCurrentUser();   // from storage.js
  if (!user) {
    borrowedContainer.innerHTML =
      '<p>Please <a href="login.html">log in</a> to view your borrowed books.</p>';
    return;
  }

  try {
    const res  = await fetch(`${API}/borrowed/`, { credentials: "include" });
    const data = await res.json();

    if (!res.ok) {
      borrowedContainer.innerHTML = `<p>${data.error || "Could not load borrowed books."}</p>`;
      return;
    }

    renderRecords(data.borrowed);
  } catch (err) {
    console.error(err);
    borrowedContainer.innerHTML = "<p>Network error. Please try again later.</p>";
  }
});
=======
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
>>>>>>> 34b9141c15628acd1892cbf72fd4e589f8fc33e4
