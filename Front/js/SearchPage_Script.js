(function () {
  "use strict";

  const state = { query: "", category: "all", availability: "all" };

  const searchInput = document.getElementById("searchInput");
  const categorySelect = document.getElementById("categoryFilter");
  const availSelect = document.getElementById("availFilter");
  const clearBtn = document.getElementById("clearBtn");
  const tbody = document.getElementById("booksTableBody");
  const visibleCountEl = document.getElementById("visibleCount");
  const totalCountEl = document.getElementById("totalCount");
  const noResults = document.getElementById("noResults");

  let allBooks = [];

  async function fetchBooks(query = "") {
    try {
      let url = `${API}/books/search/?q=${encodeURIComponent(query)}`;

      if (!query.trim()) {
        url = `${API}/books/search/?q=a`;
      }

      const response = await fetch(url);
      const data = await response.json();

      return data.results || [];
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  function renderBooks(books) {
    tbody.innerHTML = "";

    totalCountEl.textContent = books.length;
    visibleCountEl.textContent = books.length;

    if (books.length === 0) {
      noResults.style.display = "block";
      return;
    }

    noResults.style.display = "none";

    books.forEach((book) => {
      const isAvailable = book.available_copies > 0;

      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${book.title}</td>
        <td>${book.author}</td>
        <td>${book.published_date || "N/A"}</td>
        <td>${book.category || "Unknown"}</td>
        <td>${book.description || "No description"}</td>
        <td>
          <span class="badge ${isAvailable ? "badge-available" : "badge-unavailable"}">
            ${isAvailable ? "In Stock" : "Unavailable"}
          </span>
        </td>
        <td>
          <a href="book.html?id=${book.id}" class="details-link">
            Details
          </a>
        </td>
      `;

      tbody.appendChild(row);
    });
  }
})();
