

(function () {
  "use strict";

  
  const state = {
    query: "",
    category: "all",
    availability: "all",
  };

 
  const searchInput    = document.getElementById("searchInput");
  const categorySelect = document.getElementById("categoryFilter");
  const availSelect    = document.getElementById("availFilter");
  const clearBtn       = document.getElementById("clearBtn");
  const countEl        = document.getElementById("resultCount");
  const noResults      = document.getElementById("noResults");
  const tbody          = document.querySelector(".books-table tbody");

  const allRows = Array.from(tbody ? tbody.querySelectorAll("tr") : []);

  function applyFilters() {
    const q    = state.query.toLowerCase().trim();
    const cat  = state.category;
    const avail = state.availability;

    let visibleCount = 0;

    allRows.forEach((row, i) => {
      const title  = (row.dataset.title       || "").toLowerCase();
      const author = (row.dataset.author      || "").toLowerCase();
      const desc   = (row.dataset.description || "").toLowerCase();
      const rowCat = (row.dataset.category    || "").toLowerCase();
      const rowAv  = (row.dataset.availability || "").toLowerCase();

      const matchesText =
        !q ||
        title.includes(q) ||
        author.includes(q) ||
        desc.includes(q);

      const matchesCat  = cat === "all" || rowCat === cat;
      const matchesAvail = avail === "all" || rowAv === avail;

      const visible = matchesText && matchesCat && matchesAvail;

      row.style.display = visible ? "" : "none";

      if (visible) {
        
        row.style.animation = "none";
        void row.offsetHeight; 
        row.style.animation = `fadeUp 0.35s ease ${(visibleCount * 0.04)}s both`;
        visibleCount++;
      }
    });

    
    if (countEl) {
      countEl.innerHTML = `Showing <span>${visibleCount}</span> of <span>${allRows.length}</span> books`;
    }

    
    if (noResults) {
      noResults.classList.toggle("visible", visibleCount === 0);
    }

    
    const tableWrap = document.querySelector(".books-table-wrap");
    if (tableWrap) {
      tableWrap.style.display = visibleCount === 0 ? "none" : "";
    }
  }

  /
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      state.query = searchInput.value;
      applyFilters();
    });
  }

  if (categorySelect) {
    categorySelect.addEventListener("change", () => {
      state.category = categorySelect.value;
      applyFilters();
    });
  }

  if (availSelect) {
    availSelect.addEventListener("change", () => {
      state.availability = availSelect.value;
      applyFilters();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      state.query        = "";
      state.category     = "all";
      state.availability = "all";

      if (searchInput)    searchInput.value    = "";
      if (categorySelect) categorySelect.value = "all";
      if (availSelect)    availSelect.value    = "all";

      applyFilters();
    });
  }

  
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      if (searchInput) searchInput.focus();
    }
    if (e.key === "Escape" && document.activeElement === searchInput) {
      searchInput.blur();
    }
  });
  document.querySelectorAll("nav a").forEach((link) => {
    if (link.href === window.location.href) link.classList.add("active");
  });

  
  applyFilters();
})();
