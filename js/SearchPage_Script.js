(function () {
  "use strict";

  const state = { query: "", category: "all", availability: "all" };

  const searchInput = document.getElementById("searchInput");
  const categorySelect = document.getElementById("categoryFilter");
  const availSelect = document.getElementById("availFilter");
  const clearBtn = document.getElementById("clearBtn");
  const visibleCountEl = document.getElementById("visibleCount");
  const totalCountEl = document.getElementById("totalCount");
  const noResults = document.getElementById("noResults");
  const tbody = document.getElementById("booksTableBody");
  const tableWrap = document.querySelector(".books-table-wrap");

  function buildTable() {
    const books = getBooks();

    tbody.innerHTML = "";

    const categories = [...new Set(books.map((b) => b.category))].sort();
    categorySelect.innerHTML = '<option value="all">All Categories</option>';
    categories.forEach((cat) => {
      const opt = document.createElement("option");
      opt.value = cat.toLowerCase();
      opt.textContent = cat;
      categorySelect.appendChild(opt);
    });

    if (totalCountEl) totalCountEl.textContent = books.length;

    books.forEach((book, i) => {
      const isAvailable = book.availableCopies > 0;
      const avail = isAvailable ? "in stock" : "not available";

      const tr = document.createElement("tr");
      tr.dataset.title = book.title.toLowerCase();
      tr.dataset.author = book.author.toLowerCase();
      tr.dataset.description = book.description.toLowerCase();
      tr.dataset.category = book.category.toLowerCase();
      tr.dataset.availability = avail;

      tr.style.animationDelay = `${i * 0.04}s`;

      tr.innerHTML = `
        <td class="book-title-cell">${book.title}</td>
        <td class="book-author-cell">${book.author}</td>
        <td class="book-year-cell">${book.published}</td>
        <td class="book-category-cell">${book.category}</td>
        <td class="book-desc-cell"><p>${book.description}</p></td>
        <td>
          <span class="badge ${isAvailable ? "badge-available" : "badge-unavailable"}">
            ${isAvailable ? "In Stock" : "Not Available"}
          </span>
        </td>
        <td><a href="book.html?id=${book.id}" class="details-link">Details</a></td>
      `;

      tbody.appendChild(tr);
    });

    applyFilters();
  }

  function applyFilters() {
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const q = state.query.toLowerCase().trim();
    const cat = state.category;
    const avail = state.availability;

    let visible = 0;

    rows.forEach((row, i) => {
      const matchesText =
        !q ||
        row.dataset.title.includes(q) ||
        row.dataset.author.includes(q) ||
        row.dataset.description.includes(q);

      const matchesCat = cat === "all" || row.dataset.category === cat;
      const matchesAvail =
        avail === "all" || row.dataset.availability === avail;

      const show = matchesText && matchesCat && matchesAvail;
      row.style.display = show ? "" : "none";

      if (show) {
        row.style.animation = "none";
        void row.offsetHeight;
        row.style.animation = `fadeUp 0.35s ease ${visible * 0.04}s both`;
        visible++;
      }
    });

    if (visibleCountEl) visibleCountEl.textContent = visible;

    const empty = visible === 0;
    if (noResults) noResults.classList.toggle("visible", empty);
    if (tableWrap) tableWrap.style.display = empty ? "none" : "";
  }

  searchInput.addEventListener("input", () => {
    state.query = searchInput.value;
    applyFilters();
  });

  categorySelect.addEventListener("change", () => {
    state.category = categorySelect.value;
    applyFilters();
  });

  availSelect.addEventListener("change", () => {
    state.availability = availSelect.value;
    applyFilters();
  });

  clearBtn.addEventListener("click", () => {
    state.query = "";
    state.category = "all";
    state.availability = "all";
    searchInput.value = "";
    categorySelect.value = "all";
    availSelect.value = "all";
    applyFilters();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape" && document.activeElement === searchInput) {
      searchInput.blur();
    }
  });

  document.addEventListener("DOMContentLoaded", buildTable);
})();
