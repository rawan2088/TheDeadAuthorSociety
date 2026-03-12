# 📚 Online Library Website

**IS231 - Web Technology | Project 2**
This is a project made for the Web Course, at FCAI (Facility of computing and Artificial Intelligence)

---

## 👥 Team Members

| Name     | ID  | Role                                |
| -------- | --- | ----------------------------------- |
| Member 1 | -   | Home Page + Navigation Bar          |
| Member 2 | -   | Signup + Login Pages                |
| Member 3 | -   | Search + Category Pages             |
| Member 4 | -   | Book Details + Borrowed Books Pages |
| Member 5 | -   | Manage Books Page (Admin)           |
| Member 6 | -   | Add Book + Profile Pages            |

---

## 📄 Project Description

An online library web application where users can browse, search, and borrow books. The platform supports two types of users: **Admins** who manage the book catalog, and **Users** who can search and borrow books.

---

## 🔐 User Roles

### Admin

- Add, edit, and delete books
- Manage book stock and availability
- View all books and their borrow status

### User

- Browse and search for books
- View book details
- Borrow available books
- Track borrowed books

---

## 🗂️ Pages

| Page            | File                  | Access |
| --------------- | --------------------- | ------ |
| Home            | `index.html`          | All    |
| Sign Up         | `signup.html`         | All    |
| Login           | `login.html`          | All    |
| Search          | `search.html`         | All    |
| Category        | `category.html`       | All    |
| Book Details    | `book-details.html`   | User   |
| Profile         | `profile.html`        | User   |
| Borrowed Books  | `borrowed-books.html` | User   |
| Manage Books    | `manage.html`         | Admin  |
| Add / Edit Book | `add-book.html`       | Admin  |

---

## ⚙️ Technical Notes

- Built with **pure HTML and CSS only** — no frameworks allowed
- No hardcoded values; all data is entered dynamically by the user
- Navigation bar is shared across all pages and adjusts based on login state (guest / user / admin)
- Minimum 8 HTML pages — this project includes **10 pages**

---

## 📁 Folder Structure

```
project/
├── index.html
├── signup.html
├── login.html
├── search.html
├── category.html
├── book-details.html
├── profile.html
├── borrowed-books.html
├── manage.html
├── add-book.html
├── css/
│   └── style.css
└── assets/
    └── images/
```

---

## 📦 Submission

- Compressed as: `LeaderID_2_TAname_1.zip`
- Submitted by team leader via Google Classroom
- **Phase 1 Deadline: 7/3/2026**
