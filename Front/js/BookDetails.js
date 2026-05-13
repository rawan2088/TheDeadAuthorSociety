const params = new URLSearchParams(window.location.search);

const bookId = params.get("id");

const API = "http://127.0.0.1:8000/api/books";


// ---------------------------------------------------
// CHECK BOOK ID
// ---------------------------------------------------

if (!bookId) {
  document.querySelector("main").innerHTML =
    "<p>No book specified.</p>";

  throw new Error("No book id in URL");
}


// ---------------------------------------------------
// GET CURRENT USER
// ---------------------------------------------------

function getCurrentUser() {
  const user = localStorage.getItem("currentUser");

  return user ? JSON.parse(user) : null;
}


// ---------------------------------------------------
// GET CSRF TOKEN
// ---------------------------------------------------

function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== "") {

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

      cookie = cookie.trim();

      if (cookie.startsWith(name + "=")) {

        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );

        break;
      }
    }
  }

  return cookieValue;
}


// ---------------------------------------------------
// RENDER BOOK
// ---------------------------------------------------

function renderBook(book) {

  document.getElementById("bookTitle").textContent =
    book.title;

  document.getElementById("bookAuthor").textContent =
    book.author;

  document.getElementById("bookPublishedDate").textContent =
    book.published_date;

  document.getElementById("bookCategory").textContent =
    book.category;

  document.getElementById("bookDescription").textContent =
    book.description;

  document.getElementById("bookImg").src =
    book.image || "../Assets/default.jpg";


  const borrowBtn = document.getElementById("borrowBtn");

  const statusEl = document.getElementById("bookStatus");

  const user = getCurrentUser();


  // ---------------------------------------------------
  // ADMIN VIEW
  // ---------------------------------------------------

  if (user && user.role === "admin") {

    statusEl.textContent =
      `Available: ${book.availableCopies} / ${book.totalCopies}`;

    borrowBtn.style.display = "none";

    return;
  }


  // ---------------------------------------------------
  // BOOK NOT AVAILABLE
  // ---------------------------------------------------

  if (book.availableCopies <= 0) {

    statusEl.textContent = "Not Available";

    borrowBtn.textContent = "Unavailable";

    borrowBtn.disabled = true;
  }

  // ---------------------------------------------------
  // BOOK AVAILABLE
  // ---------------------------------------------------

  else {

    statusEl.textContent = "Available";

    borrowBtn.textContent = "Borrow";

    borrowBtn.disabled = false;
  }


  // ---------------------------------------------------
  // BORROW BUTTON
  // ---------------------------------------------------

  borrowBtn.addEventListener("click", () => {
    handleBorrow(book);
  });
}


// ---------------------------------------------------
// BORROW BOOK
// ---------------------------------------------------

async function handleBorrow(book) {

  const user = getCurrentUser();

  if (!user) {

    window.location.href = "login.html";

    return;
  }

  if (user.role === "admin") {

    alert("Admins cannot borrow books.");

    return;
  }

  try {

    const res = await fetch(
      `${API}/${book.id}/borrow/`,
      {
        method: "POST",

        credentials: "include",

        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      }
    );

    const data = await res.json();


    if (!res.ok || !data.success) {

      alert(data.error || "Could not borrow this book.");

      return;
    }


    alert(`"${book.title}" borrowed successfully!`);

<<<<<<< HEAD
    const borrowBtn = document.getElementById("borrowBtn");borrowBtn.textContent = "Unavailable";
    borrowBtn.disabled = true;
    document.getElementById("bookStatus").textContent = "Not Available";
=======

    const borrowBtn =
      document.getElementById("borrowBtn");


    if (data.remaining_copies <= 0) {

      borrowBtn.textContent = "Unavailable";

      borrowBtn.disabled = true;

      document.getElementById("bookStatus").textContent =
        "Not Available";
    }

>>>>>>> 77b86d4 (add member4)
  } catch (err) {

    console.error(err);

    alert("Network error. Please try again.");
  }
}


// ---------------------------------------------------
// LOAD BOOK DETAILS
// ---------------------------------------------------

document.addEventListener(
  "DOMContentLoaded",
  async () => {

    try {

      const res = await fetch(
        `${API}/${bookId}/`
      );

      if (!res.ok) {
        throw new Error("Book not found");
      }

      const data = await res.json();

      if (!data.success) {
        throw new Error(
          data.error || "Book not found"
        );
      }

      renderBook(data.book);

    } catch (err) {

      console.error(err);

      document.querySelector("main").innerHTML =
        `<p>${err.message}</p>`;
    }
  }
);
