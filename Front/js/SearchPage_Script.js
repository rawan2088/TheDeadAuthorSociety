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

  // ── Fetch books from API ──────────────────────────────────────────────────
  async function fetchBooks(query) {
    try {
      let url = `${API}/books/`; // Default URL
      if (query && query.trim()) {
        url = `${API}/books/search/?q=${encodeURIComponent(query.trim())}`;
      }

      const res = await fetch(url, { credentials: "include" });
      const data = await res.json();

      // FIX: Your Django view returns a List directly, not an object with .results
      return Array.isArray(data) ? data : data.results || [];
    } catch (err) {
      console.error("Failed to fetch books:", err);
      return [];
    }
  }

  // ── Build table rows ──────────────────────────────────────────────────────
  function buildTable(books) {
    if (!tbody) return;
    tbody.innerHTML = "";

    // Update Total Count
    if (totalCountEl) totalCountEl.textContent = books.length;

    books.forEach((book, i) => {
      const isAvailable = book.availableCopies > 0;
      const availStatus = isAvailable ? "in stock" : "not available";
      const tr = document.createElement("tr");

      // Set datasets for local filtering
      tr.dataset.category = (book.category || "").toLowerCase();
      tr.dataset.availability = availStatus;

      tr.innerHTML = `
        <td class="book-title-cell">${book.title}</td>
        <td class="book-author-cell">${book.author}</td>
        <td class="book-year-cell">${book.published_date || "N/A"}</td>
        <td class="book-category-cell">${book.category}</td>
        <td class="book-desc-cell"><p>${book.description || ""}</p></td>
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

  // ── Local filtering logic ────────────────────────────────────────────────
  function applyLocalFilters() {
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const avail = state.availability;
    let visible = 0;

    rows.forEach((row) => {
      const matchesAvail =
        avail === "all" || row.dataset.availability === avail;
      row.style.display = matchesAvail ? "" : "none";
      if (matchesAvail) visible++;
    });

    if (visibleCountEl) visibleCountEl.textContent = visible;
    const empty = visible === 0;
    if (noResults) noResults.classList.toggle("visible", empty);
    if (tableWrap) tableWrap.style.display = empty ? "none" : "";
  }

  // ── Search handler ────────────────────────────────────────────────────────
  let debounceTimer;
  async function handleSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      state.query = searchInput.value;
      const books = await fetchBooks(state.query);
      buildTable(books);
    }, 300);
  }

  // Event Listeners
  if (searchInput) searchInput.addEventListener("input", handleSearch);
  if (availSelect)
    availSelect.addEventListener("change", (e) => {
      state.availability = e.target.value;
      applyLocalFilters();
    });

  // Initial Load
  document.addEventListener("DOMContentLoaded", async () => {
    const books = await fetchBooks("");
    buildTable(books);
  });
})();
