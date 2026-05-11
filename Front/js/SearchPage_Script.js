// SearchPage_Script.js — fetches books from Django API
(function () {
  "use strict";



  const state = { query: "", category: "all", availability: "all" };

  const searchInput    = document.getElementById("searchInput");
  const categorySelect = document.getElementById("categoryFilter");
  const availSelect    = document.getElementById("availFilter");
  const clearBtn       = document.getElementById("clearBtn");
  const visibleCountEl = document.getElementById("visibleCount");
  const totalCountEl   = document.getElementById("totalCount");
  const noResults      = document.getElementById("noResults");
  const tbody          = document.getElementById("booksTableBody");
  const tableWrap      = document.querySelector(".books-table-wrap");

  // ── Fetch books from API ──────────────────────────────────────────────────
  async function fetchBooks(query) {
    try {
      let url;
      if (query && query.trim()) {
        url = `${API}/books/search/?q=${encodeURIComponent(query.trim())}`;
      } else {
        // No query — ask for all books (search with a space trick or use a
        // dedicated /api/books/ list endpoint if Member 3 added one)
        url = `${API}/books/search/?q=a`;   // broad fallback; replace with /api/books/ if available
      }
      const res  = await fetch(url, { credentials: "include" });
      const data = await res.json();
      return data.results || [];
    } catch (err) {
      console.error("Failed to fetch books:", err);
      return [];
    }
  }

  // ── Category filter (uses dedicated endpoint) ──────────────────────────────
  async function fetchByCategory(categoryName) {
    try {
      const res  = await fetch(`${API}/books/category/${encodeURIComponent(categoryName)}/`, { credentials: "include" });
      const data = await res.json();
      return data.results || [];
    } catch (err) {
      console.error("Category fetch failed:", err);
      return [];
    }
  }

  // ── Build table rows ───────────────────────────────────────────────────────
  function buildTable(books) {
    tbody.innerHTML = "";

    // Populate category dropdown from returned data
    const categories = [...new Set(books.map((b) => b.category))].sort();
    categorySelect.innerHTML = '<option value="all">All Categories</option>';
    categories.forEach((cat) => {
      const opt      = document.createElement("option");
      opt.value      = cat.toLowerCase();
      opt.textContent = cat;
      categorySelect.appendChild(opt);
    });

    if (totalCountEl) totalCountEl.textContent = books.length;

    books.forEach((book, i) => {
      const isAvailable = book.availableCopies > 0;
      const avail       = isAvailable ? "in stock" : "not available";
      const tr          = document.createElement("tr");

      tr.dataset.title        = book.title.toLowerCase();
      tr.dataset.author       = book.author.toLowerCase();
      tr.dataset.description  = (book.description || "").toLowerCase();
      tr.dataset.category     = book.category.toLowerCase();
      tr.dataset.availability = avail;
      tr.style.animationDelay = `${i * 0.04}s`;

      tr.innerHTML = `
        <td class="book-title-cell">${book.title}</td>
        <td class="book-author-cell">${book.author}</td>
        <td class="book-year-cell">${book.published_date}</td>
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

    applyLocalFilters();
  }

  // ── Client-side availability filter (runs after table is built) ────────────
  function applyLocalFilters() {
    const rows  = Array.from(tbody.querySelectorAll("tr"));
    const avail = state.availability;
    let visible = 0;

    rows.forEach((row) => {
      const matchesAvail = avail === "all" || row.dataset.availability === avail;
      row.style.display  = matchesAvail ? "" : "none";
      if (matchesAvail) {
        row.style.animation = "none";
        void row.offsetHeight;
        row.style.animation = `fadeUp 0.35s ease ${visible * 0.04}s both`;
        visible++;
      }
    });

    if (visibleCountEl) visibleCountEl.textContent = visible;
    const empty = visible === 0;
    if (noResults)  noResults.classList.toggle("visible", empty);
    if (tableWrap)  tableWrap.style.display = empty ? "none" : "";
  }

  // ── Search: debounced API call ─────────────────────────────────────────────
  let debounceTimer;
  async function handleSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      state.query = searchInput.value;
      let books;

      if (state.category !== "all") {
        // Category selected → use category endpoint, then filter by query client-side
        books = await fetchByCategory(state.category);
        if (state.query.trim()) {
          const q = state.query.toLowerCase();
          books   = books.filter(
            (b) =>
              b.title.toLowerCase().includes(q) ||
              b.author.toLowerCase().includes(q) ||
              (b.description || "").toLowerCase().includes(q)
          );
        }
      } else {
        books = await fetchBooks(state.query);
      }

      buildTable(books);
    }, 300);
  }

  // ── Category dropdown ─────────────────────────────────────────────────────
  categorySelect.addEventListener("change", async () => {
    state.category = categorySelect.value;
    handleSearch();
  });

  // ── Availability dropdown (pure client-side) ───────────────────────────────
  availSelect.addEventListener("change", () => {
    state.availability = availSelect.value;
    applyLocalFilters();
  });

  // ── Search input ───────────────────────────────────────────────────────────
  searchInput.addEventListener("input", handleSearch);

  // ── Clear button ───────────────────────────────────────────────────────────
  clearBtn.addEventListener("click", async () => {
    state.query        = "";
    state.category     = "all";
    state.availability = "all";
    searchInput.value         = "";
    categorySelect.value      = "all";
    availSelect.value         = "all";
    const books = await fetchBooks("");
    buildTable(books);
  });

  // ── Keyboard shortcuts ─────────────────────────────────────────────────────
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape" && document.activeElement === searchInput) {
      searchInput.blur();
    }
  });

  // ── Initial load ───────────────────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", async () => {
    const books = await fetchBooks("");
    buildTable(books);
  });
})();