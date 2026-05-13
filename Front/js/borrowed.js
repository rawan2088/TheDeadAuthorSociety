const borrowedContainer = document.getElementById("bookContainer");

async function handleReturn(borrowId, card) {
  if (!confirm("Are you sure you want to return this book?")) return;

  try {
    const res = await fetch(`${API}/borrowed/${borrowId}/return/`, {
      method: "POST",
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
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
      borrowedContainer.innerHTML =
        "<p>You have no borrowed books at the moment.</p>";
    }
  } catch (err) {
    console.error(err);
    alert("Network error. Please try again.");
  }
}

function renderRecords(records) {
  borrowedContainer.innerHTML = "";

  if (!records.length) {
    borrowedContainer.innerHTML = "<p>You have not borrowed any books yet.</p>";

    return;
  }

  records.forEach((record) => {
    const book = record.book;

    const card = document.createElement("div");
    card.classList.add("bookCard");

    card.innerHTML = `
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

    card.querySelector(".return-btn").addEventListener("click", () => {
      handleReturn(record.borrowId, card);
    });

    borrowedContainer.appendChild(card);
  });
}

async function loadBorrowedBooks() {
  try {
    const response = await fetch(`${API}/borrowed/`, {
      credentials: "include",
    });

    const data = await response.json();

    if (!response.ok) {
      borrowedContainer.innerHTML = `<p>${data.error || "Could not load borrowed books."}</p>`;

      return;
    }

    renderRecords(data.borrowed);
  } catch (error) {
    console.error(error);

    borrowedContainer.innerHTML =
      "<p>Network error while loading borrowed books.</p>";
  }
}

window.addEventListener("DOMContentLoaded", loadBorrowedBooks);
