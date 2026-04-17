

(function () {
  "use strict";

  /* ── Accordion logic ────────────────────────────────────── */
  function initAccordions() {
    const sections = document.querySelectorAll(".category-section");

    sections.forEach((section, idx) => {
      const header = section.querySelector(".category-header");
      const body   = section.querySelector(".category-body");
      if (!header || !body) return;

      /* open first section by default */
      if (idx === 0) openSection(header, body);

      header.addEventListener("click", () => {
        const isOpen = body.classList.contains("open");
        if (isOpen) {
          closeSection(header, body);
        } else {
          openSection(header, body);
        }
      });
    });
  }

  function openSection(header, body) {
    header.classList.add("open");
    body.classList.add("open");
  }

  function closeSection(header, body) {
    header.classList.remove("open");
    body.classList.remove("open");
  }

  /* ── Expand / Collapse All ──────────────────────────────── */
  function initExpandCollapse() {
    const btn = document.getElementById("expandCollapseBtn");
    if (!btn) return;

    let allExpanded = false;

    btn.addEventListener("click", () => {
      const sections = document.querySelectorAll(
        ".category-section:not(.hidden)"
      );
      allExpanded = !allExpanded;

      sections.forEach((section) => {
        const header = section.querySelector(".category-header");
        const body   = section.querySelector(".category-body");
        if (!header || !body) return;
        if (allExpanded) openSection(header, body);
        else closeSection(header, body);
      });

      btn.textContent = allExpanded ? "Collapse All" : "Expand All";
    });
  }

  /* ── Filter Tabs ────────────────────────────────────────── */
  function initFilterTabs() {
    const tabs     = document.querySelectorAll(".filter-tab");
    const sections = document.querySelectorAll(".category-section");

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        /* update active tab */
        tabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        const filter = tab.dataset.filter;

        sections.forEach((section) => {
          const sectionCat = section.dataset.category;

          if (filter === "all" || sectionCat === filter) {
            section.classList.remove("hidden");
            /* re-trigger fade animation */
            section.style.animation = "none";
            void section.offsetHeight;
            section.style.animation = "";
          } else {
            section.classList.add("hidden");
          }
        });
      });
    });
  }

  /* ── Active nav link ────────────────────────────────────── */
  document.querySelectorAll("nav a").forEach((link) => {
    if (link.href === window.location.href) link.classList.add("active");
  });

  /* ── Init ───────────────────────────────────────────────── */
  initAccordions();
  initFilterTabs();
  initExpandCollapse();
})();
