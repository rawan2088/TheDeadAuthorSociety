# Place at: books/tests.py

from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from borrowed.models import BorrowedBook
from .models import Book, Category, Comment

User = get_user_model()


class BookModelTests(APITestCase):
    """Tests that don't go through the API at all — pure model behavior."""

    def setUp(self):
        self.category = Category.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Dune",
            author="Frank Herbert",
            published_date="1965-01-01",
            description="A desert planet saga.",
            total_copies=3,
        )
        self.book.categories.add(self.category)
        self.user = User.objects.create_user(username="reader1", password="pass123")

    def test_book_str_returns_title(self):
        self.assertEqual(str(self.book), "Dune")

    def test_avg_rating_is_none_without_comments(self):
        self.assertIsNone(self.book.avg_rating)

    def test_avg_rating_rounds_to_two_decimals(self):
        Comment.objects.create(user=self.user, book=self.book, rating=5, content="Great")
        Comment.objects.create(user=self.user, book=self.book, rating=4, content="Good")
        Comment.objects.create(user=self.user, book=self.book, rating=4, content="Good too")
        # (5 + 4 + 4) / 3 = 4.3333... -> should round to 4.33
        self.assertEqual(self.book.avg_rating, 4.33)

    def test_category_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="Fiction")


class BookAPITests(APITestCase):
    """Tests that go through BookListView / BookDetailView, including the
    annotated available_copies field."""

    def setUp(self):
        self.category = Category.objects.create(name="Sci-Fi")
        self.book = Book.objects.create(
            title="Foundation",
            author="Isaac Asimov",
            published_date="1951-01-01",
            description="Empire falls, psychohistory rises.",
            total_copies=2,
        )
        self.book.categories.add(self.category)
        self.user = User.objects.create_user(username="borrower1", password="pass123")

    def test_book_list_returns_200(self):
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list_returns_created_book(self):
        response = self.client.get(reverse("books_list"))
        titles = [b["title"] for b in response.data]
        self.assertIn("Foundation", titles)

    def test_available_copies_with_no_borrows(self):
        response = self.client.get(reverse("books_list"))
        data = response.data[0]
        self.assertIn("available_copies", data)
        self.assertEqual(data["available_copies"], 2)

    def test_available_copies_decreases_with_active_borrow(self):
        BorrowedBook.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse("books_list"))
        data = response.data[0]
        self.assertEqual(data["available_copies"], 1)

    def test_available_copies_not_affected_by_a_returned_borrow(self):
        BorrowedBook.objects.create(
            user=self.user, book=self.book, return_date=date.today()
        )
        response = self.client.get(reverse("books_list"))
        data = response.data[0]
        # returned books shouldn't count against availability
        self.assertEqual(data["available_copies"], 2)

    def test_book_detail_returns_correct_book(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Foundation")

    def test_book_detail_404_for_missing_book(self):
        response = self.client.get(reverse("book_detail", args=[999999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)