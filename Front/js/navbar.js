// navbar.js — updated for Django backend

async function fetchCurrentUser() {
  try {
    const response = await fetch("/api/me/", {
      credentials: "include",  // sends the session cookie
    });
    if (!response.ok) return null;  // 401 = not logged in
    return await response.json();
  } catch {
    return null;
  }
}

async function handleLogout() {
  await fetch("/api/logout/", {
    method: "POST",
    credentials: "include",
  });
  sessionStorage.removeItem("currentUser");
  window.location.href = "/pages/index.html";
}

async function renderNavbar() {
  // First check sessionStorage (fast, avoids extra request on every page)
  let user = JSON.parse(sessionStorage.getItem("currentUser"));

  // If nothing in sessionStorage, ask the server (e.g. after page refresh)
  if (!user) {
    user = await fetchCurrentUser();
    if (user) {
      sessionStorage.setItem("currentUser", JSON.stringify(user));
    }
  }

  let navLinks = `
    <a href="/pages/index.html">Home</a>
    <span class="nav-divider"></span>
  `;

  if (!user) {
    navLinks += `
      <a href="/pages/login.html">Login</a>
      <a href="/pages/signup.html">Sign Up</a>
    `;
  } else if (user.role === "admin") {
    navLinks += `
      <a href="/pages/Manage.html">Manage Books</a>
      <a href="/pages/Add_Book.html">Add Book</a>
      <a href="/pages/Profile.html">My Profile</a>
      <a href="#" id="logoutBtn">Logout</a>
    `;
  } else {
    navLinks += `
      <a href="/pages/borrowed.html">My Books</a>
      <a href="/pages/Profile.html">My Profile</a>
      <a href="#" id="logoutBtn">Logout</a>
    `;
  }

  const navbarContainer = document.getElementById("navbar");
  navbarContainer.innerHTML = `
    <header>
      <div class="navbar-inner">
        <h1 id="mainLogo" onclick="window.location.href='/pages/index.html'">
          TheDeadAuthorSociety
        </h1>

        <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav id="mainNav">
          ${navLinks}
        </nav>
      </div>
    </header>

    <div class="nav-overlay" id="navOverlay"></div>
  `;

  highlightActiveLink();

  // Wire up logout button
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      handleLogout();
    });
  }

  // Hamburger toggle
  const hamburger = document.getElementById("hamburgerBtn");
  const nav = document.getElementById("mainNav");
  const overlay = document.getElementById("navOverlay");

  hamburger.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    hamburger.classList.toggle("open", isOpen);
    overlay.classList.toggle("open", isOpen);
    document.body.style.overflow = isOpen ? "hidden" : "";
  });

  overlay.addEventListener("click", closeNav);
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeNav);
  });

  function closeNav() {
    nav.classList.remove("open");
    hamburger.classList.remove("open");
    overlay.classList.remove("open");
    document.body.style.overflow = "";
  }
}

function highlightActiveLink() {
  const currentPath = window.location.pathname.split("/").pop() || "index.html";
  const links = document.querySelectorAll("#mainNav a");
  links.forEach((link) => {
    const linkPath = link.getAttribute("href").split("/").pop();
    if (linkPath === currentPath) {
      link.classList.add("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", renderNavbar);