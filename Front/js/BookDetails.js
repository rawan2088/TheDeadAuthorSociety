
const params = new URLSearchParams(window.location.search);
const bookId = params.get("id");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
}

if (!bookId) {
  document.querySelector("main").innerHTML = "<p>No book specified.</p>";
  throw new Error("No book id in URL");
}

const books = JSON.parse(localStorage.getItem("books"));
const book = books.find((b) => b.id == bookId);

if (!book) {
  document.querySelector("main").innerHTML = "<p>Book not found.</p>";
  throw new Error("Book not found");
}

function renderBook(book) {
  document.getElementById("bookTitle").textContent        = book.title;
  document.getElementById("bookAuthor").textContent       = book.author;
  document.getElementById("bookPublishedDate").textContent = book.published_date;
  document.getElementById("bookCategory").textContent     = book.category;
  document.getElementById("bookDescription").textContent  = book.description;
  document.getElementById("bookImg").src                  = book.image || "../Assets/default.jpg";

  const borrowBtn  = document.getElementById("borrowBtn");
  const statusEl   = document.getElementById("bookStatus");
  const user       = getCurrentUser();       
  if (user && user.role === "admin") {
    statusEl.textContent      = `Available: ${book.availableCopies} / ${book.totalCopies}`;
    borrowBtn.style.display   = "none";
    return;
  }

  if (book.availableCopies <= 0) {
    statusEl.textContent  = "Not Available";
    borrowBtn.textContent = "Unavailable";
    borrowBtn.disabled    = true;
  } else {
    statusEl.textContent  = "Available";
    borrowBtn.textContent = "Borrow";
    borrowBtn.disabled    = false;
  }

  borrowBtn.addEventListener("click", () => handleBorrow(book));
}


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
    const res = await fetch(`${API}/books/${book.id}/borrow/`, {
      method:      "POST",
      credentials: "include",   // send session cookie
      headers:     { "X-CSRFToken": getCookie("csrftoken") },
    });
    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "Could not borrow this book.");
      return;
    }

    alert(`"${book.title}" borrowed successfully!`);

  
    const borrowBtn = document.getElementById("borrowBtn");
    if (data.availableCopies <= 0) {
      borrowBtn.textContent = "Unavailable";
      borrowBtn.disabled    = true;
      document.getElementById("bookStatus").textContent = "Not Available";
    }
  } catch (err) {
    console.error(err);
    alert("Network error. Please try again.");
  }
}
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res  = await fetch(`${API}/books/${bookId}/`);
    if (!res.ok) throw new Error("Book not found");
    const book = await res.json();
    renderBook(book);
  } catch (err) {
    document.querySelector("main").innerHTML = `<p>${err.message}</p>`;
  }
});