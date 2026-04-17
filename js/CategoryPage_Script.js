(function () {
  "use strict";

  const container = document.getElementById("categoriesContainer");
  const filterBar = document.getElementById("filterBar");

  const categoryIcons = {
    "classic fiction",
    "southern gothic",
    "southern gothic / bildungsroman",
    bildungsroman,
    "young adult",
    "mystery thriller",
    romance,
    "classical romance",
    "self help",
    "historical fiction",
  };

  function getIcon(category) {
    return categoryIcons[category.toLowerCase()] || "📚";
  }

  function buildPage() {
    const books = getBooks();

    const grouped = {};
    books.forEach((book) => {
      const cat = book.category;
      if (!grouped[cat]) grouped[cat] = [];
      grouped[cat].push(book);
    });

    const sortedCategories = Object.keys(grouped).sort();

    filterBar
      .querySelectorAll(".filter-tab:not([data-filter='all'])")
      .forEach((t) => t.remove());
    const expandBtn = document.getElementById("expandCollapseBtn");

    sortedCategories.forEach((cat) => {
      const tab = document.createElement("button");
      tab.classList.add("filter-tab");
      tab.dataset.filter = cat.toLowerCase();
      tab.textContent = cat;
      filterBar.insertBefore(tab, expandBtn);
    });

    container.innerHTML = "";

    sortedCategories.forEach((cat, idx) => {
      const booksInCat = grouped[cat];
      const section = document.createElement("div");
      section.classList.add("category-section");
      section.dataset.category = cat.toLowerCase();
      section.style.animationDelay = `${(idx + 1) * 0.05}s`;

      const cardsHTML = booksInCat
        .map((book) => {
          const isAvailable = book.availableCopies > 0;
          return `
          <div class="book-card">
            <div class="card-title">${book.title}</div>
            <div class="card-author">${book.author}</div>
            <div class="card-meta">
              <span class="card-year">${book.published}</span>
              <span class="badge ${isAvailable ? "badge-available" : "badge-unavailable"}">
                ${isAvailable ? "In Stock" : "Not Available"}
              </span>
            </div>
            <div class="card-desc">${book.description}</div>
            <div class="card-footer">
              <a href="book.html?id=${book.id}" class="card-details-link">View Details</a>
            </div>
          </div>
        `;
        })
        .join("");

      section.innerHTML = `
        <div class="category-header">
          <div class="category-header-left">
            <div class="category-icon">${getIcon(cat)}</div>
            <div>
              <div class="category-name">${cat}</div>
              <div class="category-count">${booksInCat.length} ${booksInCat.length === 1 ? "book" : "books"}</div>
            </div>
          </div>
          <span class="category-chevron">▼</span>
        </div>
        <div class="category-body">
          <div class="book-cards-grid">${cardsHTML}</div>
        </div>
      `;

      container.appendChild(section);
    });

    initAccordions();
    initFilterTabs();
    initExpandCollapse();

    const firstHeader = container.querySelector(".category-header");
    const firstBody = container.querySelector(".category-body");
    if (firstHeader && firstBody) openSection(firstHeader, firstBody);
  }

  function openSection(header, body) {
    header.classList.add("open");
    body.classList.add("open");
  }

  function closeSection(header, body) {
    header.classList.remove("open");
    body.classList.remove("open");
  }

  function initAccordions() {
    container.querySelectorAll(".category-section").forEach((section) => {
      const header = section.querySelector(".category-header");
      const body = section.querySelector(".category-body");
      if (!header || !body) return;

      header.addEventListener("click", () => {
        if (body.classList.contains("open")) closeSection(header, body);
        else openSection(header, body);
      });
    });
  }

  function initExpandCollapse() {
    const btn = document.getElementById("expandCollapseBtn");
    if (!btn) return;
    let allExpanded = false;

    btn.addEventListener("click", () => {
      allExpanded = !allExpanded;
      container
        .querySelectorAll(".category-section:not(.hidden)")
        .forEach((section) => {
          const header = section.querySelector(".category-header");
          const body = section.querySelector(".category-body");
          if (!header || !body) return;
          if (allExpanded) openSection(header, body);
          else closeSection(header, body);
        });
      btn.textContent = allExpanded ? "Collapse All" : "Expand All";
    });
  }

  function initFilterTabs() {
    filterBar.addEventListener("click", (e) => {
      const tab = e.target.closest(".filter-tab");
      if (!tab) return;

      filterBar
        .querySelectorAll(".filter-tab")
        .forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const filter = tab.dataset.filter;

      container.querySelectorAll(".category-section").forEach((section) => {
        const matches = filter === "all" || section.dataset.category === filter;
        section.classList.toggle("hidden", !matches);
        if (matches) {
          section.style.animation = "none";
          void section.offsetHeight;
          section.style.animation = "";
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", buildPage);
})();
