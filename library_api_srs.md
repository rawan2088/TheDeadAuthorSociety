# Software Requirements Specification
## Library Website API

**Version:** 0.1 (Draft)
**Status:** Open questions noted inline — see Section 7

---

## 1. Introduction

### 1.1 Purpose
This SRS defines the functional and access-control requirements for a library management API built on Django/DRF. It covers user roles, book cataloging, borrowing rules, comments, and the resulting REST surface.

### 1.2 Scope
The system manages books, categories, borrowing records, and user-submitted ratings/comments. It exposes a REST API consumed by a separate frontend client.

---

## 2. User Roles

| Role | Backing field | Can browse/borrow/comment | Can manage books | Can manage users |
|---|---|---|---|---|
| **Normal user** | `is_admin=False` | Yes | No | No (self only: profile, own borrow history) |
| **Admin** | `is_admin=True` | Yes | Yes | Yes |

Currently the schema only distinguishes two tiers via the single `is_admin` boolean. A **staff/librarian** tier (can manage books and borrowing, but not create/delete other users) is *not yet modeled*. See Section 7.1 for the decision this requires before implementation.

---

## 3. Functional Requirements

### 3.1 Books
- **FR-1**: A book may belong to multiple categories (`Book.categories`, M2M).
- **FR-2**: A book has multiple physical copies (`total_copies`); the system must expose how many are currently available (`available_copies = total_copies − active borrow count`).
- **FR-3**: A book cannot be borrowed when `available_copies == 0`.

### 3.2 Categories
- **FR-4**: Category names are unique.
- **FR-5**: The API must support listing all categories and, for a given category, listing the books tagged with it.

### 3.3 Borrowing
- **FR-6**: A user may hold at most **5 active** (unreturned) borrow records at any time.
- **FR-7**: A user cannot hold two *simultaneous* active borrows of the *same* book — enforced today via a partial unique constraint on `(user, book) WHERE return_date IS NULL`.
- **FR-8**: A user **may** re-borrow a book they previously returned — the constraint above only blocks concurrent active borrows, not repeat borrows over time.
- **FR-9**: A returned book's `BorrowedBook` row is **not deleted** — it remains as historical record, distinguished from active borrows by `return_date IS NOT NULL`.

### 3.4 Comments
- **FR-10**: A comment carries a numeric rating. Rating must be constrained to a valid range (e.g., 1–5) — not currently enforced at the model level (see prior schema review).
- **FR-11**: A comment is tied to one user and one book.

---

## 4. Authorization Rules

### 4.1 Books — Create / Edit / Delete
- Only **Admins** (`is_admin=True`) may create, update, or delete `Book` and `Category` records.
- All authenticated users (and optionally anonymous users) may **read** books/categories.
- Normal users interact with books only by borrowing and commenting — never by editing catalog data.

### 4.2 Users — Delete
- Only **Admins** may delete other user accounts.
- A user may typically deactivate/delete their *own* account (soft-delete recommended — see 4.3).
- Superuser/self-protection: an admin should not be able to delete the last remaining admin account (business rule to enforce in the view layer, not the DB).

### 4.3 Deletion Cascade Behavior

| Deleted entity | Effect today (`on_delete`) | Consequence |
|---|---|---|
| **Book** deleted | `Comment.book` → `CASCADE`, `BorrowedBook.book` → `CASCADE` | All comments and *all* borrow history (active + returned) for that book are erased. |
| **User** deleted | `Comment.user` → `SET_NULL`, `BorrowedBook.user` → `CASCADE` | Comments survive as orphaned/anonymized; **but all borrow history, including returned records, is erased.** |

⚠️ **Conflict flagged**: FR-9 requires returned borrows to persist as history, but `BorrowedBook.user` is currently `on_delete=CASCADE`, so deleting a user silently destroys that history. Two ways to resolve, pick one:
- Change `BorrowedBook.user` to `on_delete=SET_NULL` (with `null=True`) so records survive user deletion, same pattern already used for `Comment.user`.
- Or treat user deletion as **soft-delete only** (`is_active=False`) and never hard-delete a user with borrow history — simpler, no schema change needed, but requires enforcing "no hard delete" in the view/permission layer.

Recommend the first option if audit/history matters even after account deletion; the second if user deletion should be rare/administrative only.

---

## 5. API Surface

### 5.1 Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/` — current user profile

### 5.2 Books
- `GET /api/books/` — list, filterable by `category`, `author`, search by title
- `GET /api/books/{id}/` — detail, includes `available_copies`, categories, and comments
- `POST /api/books/` — Admin only
- `PATCH /api/books/{id}/` — Admin only
- `DELETE /api/books/{id}/` — Admin only

### 5.3 Categories
- `GET /api/categories/` — **categories page**: list all categories, each with a book count
- `GET /api/categories/{id}/` — **single category page**: category detail + paginated list of its books
- `POST /api/categories/` — Admin only
- `DELETE /api/categories/{id}/` — Admin only

### 5.4 Borrowing
- `GET /api/borrowed/` — current user's borrow history (active + returned); Admin can filter by `user`
- `POST /api/borrowed/` — borrow a book (validates FR-6, FR-7, and `available_copies > 0`)
- `PATCH /api/borrowed/{id}/return/` — mark returned (sets `return_date`)

### 5.5 Comments
- `GET /api/books/{id}/comments/`
- `POST /api/books/{id}/comments/` — authenticated users
- `DELETE /api/comments/{id}/` — comment owner or Admin

### 5.6 Users (Admin)
- `GET /api/users/` — Admin only
- `DELETE /api/users/{id}/` — Admin only

---

## 6. Non-Functional Notes
- Borrow-limit (FR-6) and same-book-concurrency (FR-7) checks must run at the application/serializer layer for the count-based rule, backed by the DB partial unique index for the concurrency rule as a hard guarantee.
- Rating bounds (FR-10) should be enforced both in the serializer and as a DB `CHECK` constraint.

---

## 7. Open Questions

### 7.1 Is a "staff" tier worth adding?
Right now `is_admin` is a single boolean, so the only choice is *regular user* or *full admin*. Add a staff tier if you want a role that can manage the catalog (books/categories) and process borrow/return actions, **without** being able to touch other user accounts — a "librarian" role, distinct from full admin. Skip it if a single admin type is enough for your use case (e.g., a small deployment where you're the only person managing the catalog).

If added, two implementation paths:
- **Simplest**: a second boolean, `is_staff_member` (careful not to collide with Django's built-in `is_staff`, which controls Django-admin-site access, not your API permissions).
- **More scalable**: replace the boolean with a `role` field (`CharField` + `TextChoices`: `user` / `staff` / `admin`), which reads more clearly in permission checks (`request.user.role == 'admin'`) and leaves room for a fourth tier later without another migration.
