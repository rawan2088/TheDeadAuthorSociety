from django.db import models
from django.contrib.auth.models import AbstractUser


# ---------------------------------------------------
# CUSTOM USER
# ---------------------------------------------------

class User(AbstractUser):

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ---------------------------------------------------
# CATEGORY
# ---------------------------------------------------

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name


# ---------------------------------------------------
# BOOK
# ---------------------------------------------------

class Book(models.Model):

    title = models.CharField(max_length=255)

    author = models.CharField(max_length=255)

    published_date = models.DateField()

    description = models.TextField()

    image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )

    category = models.ForeignKey(

        Category,

        on_delete=models.SET_NULL,

        null=True,

        related_name='books'
    )

    totalCopies = models.PositiveIntegerField(
        default=1
    )

    availableCopies = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):

        return self.title


# ---------------------------------------------------
# BORROWED BOOKS
# ---------------------------------------------------

class BorrowedBooks(models.Model):

    userId = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='borrowed_books'
    )

    bookId = models.ForeignKey(

        Book,

        on_delete=models.CASCADE,

        related_name='borrow_records'
    )

    borrowed_date = models.DateField(
        auto_now_add=True
    )

    return_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.userId.username} borrowed {self.bookId.title}"


# ---------------------------------------------------
# COMMENTS
# ---------------------------------------------------

class Comment(models.Model):

    userId = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    bookId = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    username = models.CharField(max_length=255)

    rating = models.IntegerField()

    content = models.TextField()

    def __str__(self):

        return f"{self.username} - {self.bookId.title}"