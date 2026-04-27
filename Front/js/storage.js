// This is the central js page, which contains all the main functions related to local storage
// We would keep use the local storage only, since json files, which were my initial thoughts, are only really efficient in backend.

const seedBooks = [
  {
    id: 1,
    title: "The Great Gatsby",
    author: "F. Scott Fitzgerald",
    published: 1925,
    category: "Classic Fiction",
    description:
      "Published in 1925, The Great Gatsby is a classic piece of American fiction told from the perspective of Nick Carraway about the eponymous Jay Gatsby, set over a few months in 1922.",
    image: "../Assets/book1.webp",
    totalCopies: 5,
    availableCopies: 5,
  },
  {
    id: 2,
    title: "To Kill A Mockingbird",
    author: "Harper Lee",
    published: 1960,
    category: "Southern Gothic",
    description:
      "Set in small-town Alabama, the novel chronicles the childhood of Scout and Jem Finch as their father Atticus defends a Black man falsely accused of rape.",
    image: "../Assets/book2.jpg",
    totalCopies: 4,
    availableCopies: 4,
  },
  {
    id: 3,
    title: "Call It What You Want",
    author: "Brigid Kemmerer",
    published: 2023,
    category: "Young Adult",
    description:
      "When his dad is caught embezzling funds from half the town, Rob goes from popular lacrosse player to social pariah, while Maegan hides secrets of her own.",
    image: "../Assets/book3.jpg",
    totalCopies: 3,
    availableCopies: 0,
  },
  {
    id: 4,
    title: "A Good Girl's Guide To Murder",
    author: "Holly Jackson",
    published: 2019,
    category: "Mystery Thriller",
    description:
      "Five years ago, schoolgirl Andie Bell was murdered by Sal Singh — or so everyone believes. Pippa Fitz-Amobi isn't convinced and starts digging for the truth.",
    image: "../Assets/book4.jpg",
    totalCopies: 6,
    availableCopies: 6,
  },
  {
    id: 5,
    title: "Betting on You",
    author: "Lynn Painter",
    published: 2023,
    category: "Romance",
    description:
      "When seventeen-year-old Bailey starts a new job at a hotel waterpark, she runs into Charlie — an old acquaintance whose cynicism clashes with her careful temperament.",
    image: "../Assets/book5.jpg",
    totalCopies: 3,
    availableCopies: 0,
  },
  {
    id: 6,
    title: "Pride and Prejudice",
    author: "Jane Austen",
    published: 1813,
    category: "Classical Romance",
    description:
      "Jane Austen's much-adapted novel is famed for its witty, spirited heroine and sensational romances, with deft remarks on the triumphs and pitfalls of social convention.",
    image: "../Assets/book6.jpg",
    totalCopies: 5,
    availableCopies: 5,
  },
  {
    id: 7,
    title: "Steal Like an Artist",
    author: "Austin Kleon",
    published: 2012,
    category: "Self Help",
    description:
      "A manifesto for the digital age — a guide with positive messages, illustrations, and exercises that puts readers directly in touch with their artistic side.",
    image: "../Assets/book7.jpg",
    totalCopies: 4,
    availableCopies: 0,
  },
  {
    id: 8,
    title: "The Silent Patient",
    author: "Alex Michaelides",
    published: 2019,
    category: "Mystery Thriller",
    description:
      "Alicia Berenson's life seems perfect until she shoots her husband five times in the face — and then never speaks another word.",
    image: "../Assets/book8.jpg",
    totalCopies: 5,
    availableCopies: 5,
  },
  {
    id: 9,
    title: "Little Women",
    author: "Louisa May Alcott",
    published: 1868,
    category: "Historical Fiction",
    description:
      "Generations of readers have fallen in love with the March sisters — Jo, Beth, Meg, and Amy — united in devotion to each other during the Civil War era.",
    image: "../Assets/book9.jpg",
    totalCopies: 4,
    availableCopies: 0,
  },
];

const seedUsers = [
  {
    id: 1,
    firstName: "Admin",
    lastName: "User",
    username: "admin",
    password: "admin123",
    email: "admin@deadauthorsociety.com",
    role: "admin",
  },
  {
    id: 2,
    firstName: "Rawan",
    lastName: "Ahmed",
    username: "Rawan",
    password: "123456",
    email: "rawan@gmail.com",
    role: "admin",
  },
  {
    id: 3,
    firstName: "Roaa",
    lastName: "AbdElFatah",
    username: "Roaa",
    password: "123456",
    email: "roaa@gmail.com",
    role: "user",
  },
  {
    id: 4,
    firstName: "Maryam",
    lastName: "Ahmed",
    username: "Maryam",
    password: "123456",
    email: "maryam@gmail.com",
    role: "user",
  },
];

const seedComments = [
  {
    id: 1,
    bookId: 1,
    username: "Roaa",
    rating: 5,
    comment: "An absolute masterpiece. Highly recommend to everyone!",
    date: "2024-01-15",
  },
  {
    id: 2,
    bookId: 1,
    username: "Rawan",
    rating: 4,
    comment: "A great read, kept me engaged from start to finish.",
    date: "2024-02-20",
  },
  {
    id: 3,
    bookId: 2,
    username: "Roaa",
    rating: 5,
    comment: "One of the most important books I have ever read.",
    date: "2024-03-10",
  },
  {
    id: 4,
    bookId: 4,
    username: "Rawan",
    rating: 5,
    comment: "Could not put it down. Finished it in one sitting!",
    date: "2024-04-05",
  },
  {
    id: 5,
    bookId: 6,
    username: "Roaa",
    rating: 5,
    comment: "A timeless classic. Elizabeth Bennet is iconic.",
    date: "2024-05-18",
  },
  {
    id: 6,
    bookId: 8,
    username: "Rawan",
    rating: 5,
    comment: "The twist at the end blew my mind completely.",
    date: "2024-06-22",
  },
];

const seedBorrowed = [
  {
    id: 1,
    userId: 2,
    bookId: 3,
    borrowDate: "2024-06-01",
  },
  {
    id: 2,
    userId: 2,
    bookId: 5,
    borrowDate: "2024-06-15",
  },
  {
    id: 3,
    userId: 3,
    bookId: 7,
    borrowDate: "2024-07-01",
  },
  {
    id: 4,
    userId: 3,
    bookId: 9,
    borrowDate: "2024-07-10",
  },
];

function initializeData() {
  if (!localStorage.getItem("books")) {
    localStorage.setItem("books", JSON.stringify(seedBooks));
  }
  if (!localStorage.getItem("users")) {
    localStorage.setItem("users", JSON.stringify(seedUsers));
  }
  if (!localStorage.getItem("comments")) {
    localStorage.setItem("comments", JSON.stringify(seedComments));
  }

  if (!localStorage.getItem("borrowed")) {
    localStorage.setItem("borrowed", JSON.stringify(seedBorrowed));
  }
}

initializeData();

function getUsers() {
  return JSON.parse(localStorage.getItem("users")) || [];
} // login + signup both need this

function saveUser(user) {
  let users = getUsers();

  if (user.id == null) {
    const ids = users.map((b) => b.id);
    user.id = users.length > 0 ? Math.max(...ids) + 1 : 1;
  }

  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));

  return true;
} // signup needs this

function getUserByUsername(name) {
  let users = getUsers();
  return users.find((u) => u.username == name);
} // login needs this
// returns the object of the user with the given username

function updateUser(updatedUser) {
  let users = getUsers();
  let index = users.findIndex((u) => u.id === updatedUser.id);

  users[index] = updatedUser;

  localStorage.setItem("users", JSON.stringify(users));
  return updatedUser;
}
// profile page needs this

// BOOKS
function getBooks() {
  return JSON.parse(localStorage.getItem("books")) || [];
} // home, search, manage, book template all need this

function saveBook(book) {
  let books = getBooks();
  books.push(book);
  localStorage.setItem("books", JSON.stringify(books));

  return books;
}

function getBookById(id) {
  let books = getBooks();
  return books.find((b) => b.id == id);
}
// book template + manage need this

function updateBook(updatedBook) {
  let books = getBooks();
  let index = books.findIndex((b) => b.id === updatedBook.id);

  books[index] = updatedBook;

  localStorage.setItem("books", JSON.stringify(books));
} // manage (edit + add copies) needs this

function deleteBook(id) {
  let books = getBooks();
  books = books.filter((b) => b.id != id); // returns the books without that id

  localStorage.setItem("books", JSON.stringify(books));
} // manage needs this

// BORROWED
function borrowBook(userId, bookId) {
  const book = getBookById(bookId);
  if (book.availableCopies <= 0) {
    alert("Sorry, no copies available for this book.");
    return;
  }
  let borrowed = JSON.parse(localStorage.getItem("borrowed")) || [];

  const ids = borrowed.map((b) => b.id);
  borrowed.push({
    id: borrowed.length > 0 ? Math.max(...ids) + 1 : 1,
    userId: parseInt(userId),
    bookId: parseInt(bookId),
    borrowDate: new Date().toISOString().split("T")[0],
  });

  book.availableCopies -= 1;
  updateBook(book);

  localStorage.setItem("borrowed", JSON.stringify(borrowed));
} // book details needs this

function getBorrowedByUser(user) {
  let borrowed = JSON.parse(localStorage.getItem("borrowed")) || [];

  return borrowed.filter((b) => b.userId == user.id);
} // borrowed-books page needs this

function isBookBorrowed(userId, bookId) {
  let borrowed = JSON.parse(localStorage.getItem("borrowed")) || [];
  return borrowed.some((b) => b.userId == userId && b.bookId == bookId);
} // book details needs this (to disable button)

function returnBook(borrowId) {
  let borrowed = JSON.parse(localStorage.getItem("borrowed")) || [];

  const record = borrowed.find((b) => b.id == borrowId);
  if (!record) return;

  // Give the copy back
  const book = getBookById(record.bookId);
  if (book) {
    book.availableCopies += 1;
    updateBook(book);
  }

  // Remove the borrow record
  borrowed = borrowed.filter((b) => b.id != borrowId);
  localStorage.setItem("borrowed", JSON.stringify(borrowed));
}

// COMMENTS
function saveComment(comment) {
  let comments = JSON.parse(localStorage.getItem("comments")) || [];
  comments.push(comment);
  localStorage.setItem("comments", JSON.stringify(comments));
} // book details needs this

function getCommentsByBook(bookId) {
  let comments = JSON.parse(localStorage.getItem("comments")) || [];
  return comments.filter((c) => c.bookId == bookId);
} // book details needs this

// CURRENT USER (sessionStorage)
function setCurrentUser(user) {
  sessionStorage.setItem("currentUser", JSON.stringify(user)); // we save the whole
} // login needs this

function getCurrentUser() {
  return JSON.parse(sessionStorage.getItem("currentUser"));
} // every page needs this for the navbar

function logoutUser() {
  sessionStorage.removeItem("currentUser");
} // logout button needs this

// export {
//   getUsers,
//   saveUser,
//   getUserByUsername,
//   updateUser,
//   getBooks,
//   saveBook,
//   getBookById,
//   updateBook,
//   deleteBook,
//   borrowBook,
//   getBorrowedByUser,
//   isBookBorrowed,
//   saveComment,
//   getCommentsByBook,
//   setCurrentUser,
//   getCurrentUser,
//   logoutUser,
// };
