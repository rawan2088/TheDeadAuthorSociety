// import { getCurrentUser, logoutUser } from "./storage.js";
// function renderNavbar() {
//   const user = getCurrentUser();

//   let links = `
//     <a href="../index.html">Home</a>
//   `;

//   if (!user) {
//     links += `
//       <a href="../login.html">Login</a>
//       <a href="../signup.html">Sign Up</a>
//     `;
//   } else if (user.role === "admin") {
//     links += `
//       <a href="../Manage.html">Manage Books</a>
//       <a href="../Add_Book.html">Add Book</a>
//       <a href="../Profile.html">My Profile</a>
//       <button onclick="handleLogout()">Logout</button>
//     `;
//   } else {
//     links += `
//       <a href="../borrowed.html">My Books</a>
//       <a href="../Profile.html">My Profile</a>
//       <button onclick="handleLogout()">Logout</button>
//     `;
//   }

//   document.getElementById("navbar").innerHTML = `
//     <header>
//       <h1 id="mainLogo">TheDeadAuthorSociety</h1>
//       <nav>${links}</nav>
//     </header>
//   `;
// }

// function handleLogout() {
//   logoutUser();
//   window.location.href = "../index.html";
// }

const navbarContainer = document.getElementById("navbar");
function renderNavbar() {
  const user = getCurrentUser();

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

  navbarContainer.innerHTML = `
    <header>
      <div class="navbar-inner">
        <h1 id="mainLogo" onclick="window.location.href='.//index.html'">
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

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      handleLogout();
    });
  }

  // --- hamburger toggle ---
  const hamburger = document.getElementById("hamburgerBtn");
  const nav = document.getElementById("mainNav");
  const overlay = document.getElementById("navOverlay");

  hamburger.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");

    // whatever the state is, toggle the same state on all related elements
    hamburger.classList.toggle("open", isOpen);
    overlay.classList.toggle("open", isOpen);

    // prevent body scroll when drawer is open
    document.body.style.overflow = isOpen ? "hidden" : "";
  });

  // close drawer when clicking the overlay
  overlay.addEventListener("click", closeNav);

  // close drawer when a nav link is clicked (on mobile)
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
  console.log(currentPath);
  const links = document.querySelectorAll("#mainNav a");
  links.forEach((link) => {
    const linkPath = link.getAttribute("href").split("/").pop();
    if (linkPath === currentPath) {
      link.classList.add("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", renderNavbar);
