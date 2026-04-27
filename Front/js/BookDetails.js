const params = new URLSearchParams(window.location.search);
const bookId = params.get("id");

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

document.getElementById("bookTitle").textContent = book.title;
document.getElementById("bookAuthor").textContent = book.author;
document.getElementById("bookPublishedDate").textContent = book.published;
document.getElementById("bookCategory").textContent = book.category;
document.getElementById("bookStatus").textContent =
  book.availableCopies > 0 ? "Available" : "Not Available";
document.getElementById("bookDescription").textContent = book.description;
document.getElementById("bookImg").src = book.image;

let borrowBtn = document.getElementById("borrowBtn");

const user = getCurrentUser();

if (user.role == "admin") {
  console.log("Admin viewing book details - hiding borrow button");
  bookStatus.textContent = `Available Copies: ${book.availableCopies} - 
  Total Copies: ${book.totalCopies}`;
  borrowBtn.style.display = "none";
}

if (book.availableCopies <= 0) {
  borrowBtn.textContent = "Unavailable";
  borrowBtn.disabled = true;
} else {
  borrowBtn.textContent = "Borrow";
  borrowBtn.disabled = false;
}

borrowBtn.addEventListener("click", () => {
  const user = getCurrentUser();

  if (!user) {
    // Not logged in — send to login
    window.location.href = "login.html";
    return;
  }

  if (user.role === "admin") {
    alert("Admins cannot borrow books.");
    return;
  }

  if (isBookBorrowed(user.id, book.id)) {
    alert("You have already borrowed this book.");
    return;
  }

  if (book.availableCopies <= 0) {
    alert("Sorry, this book is currently unavailable.");
    return;
  }

  borrowBook(user.id, book.id);
  alert(`"${book.title}" has been borrowed successfully!`);

  const updatedBooks = JSON.parse(localStorage.getItem("books")) || [];

  // you can borrow the same book twice if there are multiple copies, so check availability again
  const updatedBook = updatedBooks.find((b) => b.id == bookId);
  if (updatedBook && updatedBook.availableCopies <= 0) {
    borrowBtn.textContent = "Unavailable";
    borrowBtn.disabled = true;
    document.getElementById("bookStatus").textContent = "Not Available";
  }
});
