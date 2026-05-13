const params = new URLSearchParams(window.location.search);
const bookId = params.get("id");

if (!bookId) {
  document.querySelector("main").innerHTML = "<p>No book specified.</p>";
  throw new Error("No book id in URL");
}

function renderBook(book) {
  document.getElementById("bookTitle").textContent = book.title;
  document.getElementById("bookAuthor").textContent = book.author;
  document.getElementById("bookPublishedDate").textContent =
    book.published_date;
  document.getElementById("bookCategory").textContent = book.category;
  document.getElementById("bookDescription").textContent = book.description;
  document.getElementById("bookImg").src =
    book.image || "../Assets/default.jpg";

  const borrowBtn = document.getElementById("borrowBtn");
  const statusEl = document.getElementById("bookStatus");
  const user = getCurrentUser();
  if (user && user.role === "admin") {
    statusEl.textContent = `Available: ${book.availableCopies} / ${book.totalCopies}`;
    borrowBtn.style.display = "none";
    return;
  }

  if (book.availableCopies <= 0) {
    statusEl.textContent = "Not Available";
    borrowBtn.textContent = "Unavailable";
    borrowBtn.disabled = true;
  } else {
    statusEl.textContent = "Available";
    borrowBtn.textContent = "Borrow";
    borrowBtn.disabled = false;
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
      method: "POST",
      credentials: "include",
      credentials: "include", // send session cookie
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    });
    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "Could not borrow this book.");
      return;
    }

    alert(`"${book.title}" borrowed successfully!`);

    const borrowBtn = document.getElementById("borrowBtn");
    borrowBtn.textContent = "Unavailable";
    borrowBtn.disabled = true;
    document.getElementById("bookStatus").textContent = "Not Available";
  } catch (err) {
    console.error(err);
    alert("Network error. Please try again.");
  }
}
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch(`${API}/books/${bookId}/`);
    if (!res.ok) throw new Error("Book not found");
    const book = await res.json();
    renderBook(book);
    loadComments();
    setupCommentForm();
  } catch (err) {
    document.querySelector("main").innerHTML = `<p>${err.message}</p>`;
  }
});

async function loadComments() {
  const res = await fetch(`${API}/books/${bookId}/comments/`);
  const data = await res.json();
  const list = document.getElementById("commentsList");
  list.innerHTML = "";

  if (data.length === 0) {
    list.innerHTML = "<p>No comments yet.</p>";
    return;
  }

  data.forEach((comment) => {
    const div = document.createElement("div");
    div.innerHTML = `
      <strong>${comment.username}</strong>
      ${"⭐".repeat(comment.rating)}
      <p>${comment.content}</p>
      <small>${comment.created_at}</small>
      <hr>
    `;
    list.appendChild(div);
  });
}

function setupCommentForm() {
  const submitBtn = document.getElementById("submitCommentBtn");
  submitBtn.addEventListener("click", async () => {
    const rating = document.getElementById("commentRating").value;
    const content = document.getElementById("commentContent").value.trim();
    const msg = document.getElementById("commentMsg");

    if (!content) {
      msg.textContent = "Please write a comment first.";
      return;
    }

    try {
      const res = await fetch(`${API}/books/${bookId}/comments/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // Required for Django
        },
        credentials: "include", // Required to send the user session
        body: JSON.stringify({ rating, content }),
      });

      const data = await res.json();
      if (res.ok) {
        msg.textContent = "Comment added!";
        document.getElementById("commentContent").value = "";
        loadComments(); // Refresh list
      } else {
        msg.textContent = data.error || "Login to post a comment.";
      }
    } catch (err) {
      msg.textContent = "Network error.";
    }
  });
}
