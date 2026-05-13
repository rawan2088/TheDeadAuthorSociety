function renderBookCards(books, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  if (books.length === 0) {
    container.innerHTML = `<p class="empty-state">No books found.</p>`;
    return;
  }

  books.forEach((book) => {
    const isAvailable = book.availableCopies > 0;

    const card = document.createElement("div");
    card.classList.add("bookCard");

    card.innerHTML = `
      <img src="${book.image}" alt="${book.title}" />
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Category:</strong> ${book.category}</p>
      <p class="card-desc">${book.description}</p>
      <span class="badge ${isAvailable ? "badge-available" : "badge-unavailable"}">
        ${isAvailable ? "Available" : "Unavailable"}
      </span>
    `;

    // invisible anchor — covers the whole card
    const link = document.createElement("a");
    link.classList.add("invisible-link");
    link.href = `./book.html?id=${book.id}`;
    card.appendChild(link);

    container.appendChild(card);
  });
}

function getRecentBooks(books, count = 3) {
  // last N books added (by id descending)
  return books
    .slice()
    .sort((a, b) => b.id - a.id)
    .slice(0, count);
}

function getPopularBooks(books, count = 3) {
  // most borrowed = lowest availableCopies relative to totalCopies
  return books
    .slice()
    .sort((a, b) => {
      const ratioA = a.availableCopies / a.totalCopies;
      const ratioB = b.availableCopies / b.totalCopies;
      return ratioA - ratioB;
    })
    .slice(0, count);
}

// helper to fetch borrowed books from Django
async function fetchBorrowedBooks() {
  try {
    const response = await fetch(`${API}/borrowed/`, {
      credentials: "include",
    });
    if (!response.ok) return [];
    return await response.json();
  } catch (err) {
    console.error("Failed to fetch borrowed books", err);
    return [];
  }
}

async function getRecommendedBooks(books, count = 3) {
  const allBooks = books;
  const user = getCurrentUser();
  let recBooks;

  if (user) {
    const borrowedData = await fetchBorrowedBooks();
    if (borrowedData) {
      const borrowedIds = borrowedData["borrowed"].map((b) => b.book_id);
      recBooks = allBooks.filter((b) => !borrowedIds.includes(b.id));
    }

    // if user has borrowed everything, return all
    const pool = recBooks.length > 0 ? recBooks : allBooks;

    return pool.sort(() => Math.random() - 0.5).slice(0, count);
  }
  // guest just random picks
  return allBooks.sort(() => Math.random() - 0.5).slice(0, count);
}

document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch(`${API}/books/`, { credentials: "include" });
  const books = await res.json(); // this is the full array from Django

  // pass books directly instead of calling getBooks() internally
  renderBookCards(getRecentBooks(books, 3), "recentBooks");
  renderBookCards(getPopularBooks(books, 3), "popularBooks");
  renderBookCards(await getRecommendedBooks(books, 3), "recommendedBooks");
});
