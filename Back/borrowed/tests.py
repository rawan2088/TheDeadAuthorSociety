# Place at: borrowed/tests.py
#
# NOTE: these tests assume the fix to BorrowedBook.save() has been applied
# (using timezone.now().date() instead of self.borrow_date, which is still
# None at the point the override runs). See the note in chat for details --
# without the fix, test_due_date_auto_set_to_two_weeks_after_borrow and
# every other test that calls BorrowedBook.objects.create() will fail with
# TypeError instead of a normal assertion failure.

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from .models import BorrowedBook

User = get_user_model()


class BorrowedBookModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass123")
        self.book = Book.objects.create(
            title="1984",
            author="George Orwell",
            published_date="1949-06-08",
            description="Dystopian classic.",
            total_copies=1,
        )

    def test_due_date_auto_set_to_two_weeks_after_borrow(self):
        record = BorrowedBook.objects.create(user=self.user, book=self.book)
        self.assertEqual(record.due_date, record.borrow_date + timedelta(days=14))

    def test_is_returned_false_when_no_return_date(self):
        record = BorrowedBook.objects.create(user=self.user, book=self.book)
        self.assertFalse(record.is_returned)

    def test_is_returned_true_once_returned(self):
        record = BorrowedBook.objects.create(
            user=self.user, book=self.book, return_date=date.today()
        )
        self.assertTrue(record.is_returned)

    def test_cannot_have_two_active_borrows_of_same_book(self):
        BorrowedBook.objects.create(user=self.user, book=self.book)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                BorrowedBook.objects.create(user=self.user, book=self.book)

    def test_can_reborrow_after_returning(self):
        first = BorrowedBook.objects.create(
            user=self.user, book=self.book, return_date=date.today()
        )
        second = BorrowedBook.objects.create(user=self.user, book=self.book)
        self.assertIsNone(second.return_date)
        self.assertNotEqual(first.id, second.id)

    def test_return_date_before_borrow_date_is_rejected(self):
        # borrow_date is always stamped "today" via auto_now_add, so any
        # return_date in the past should trip chk_return_after_borrow
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                BorrowedBook.objects.create(
                    user=self.user,
                    book=self.book,
                    return_date=date.today() - timedelta(days=1),
                )


class BorrowedBooksAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass123")
        self.other_user = User.objects.create_user(username="carol", password="pass123")
        self.book = Book.objects.create(
            title="Brave New World",
            author="Aldous Huxley",
            published_date="1932-01-01",
            description="Dystopian classic #2.",
            total_copies=5,
        )
        self.record = BorrowedBook.objects.create(user=self.user, book=self.book)

    def test_borrowed_books_list_returns_200(self):
        response = self.client.get(reverse("borrowed_books"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrowed_books_list_returns_all_records(self):
        # BorrowedBooksListAPIView currently has no user-based filtering and
        # no permission_classes -- this test documents that as its current
        # behavior. If that's not intentional, this is worth revisiting:
        # right now anyone (even unauthenticated) can see every user's
        # borrow history via this endpoint.
        BorrowedBook.objects.create(
            user=self.other_user,
            book=Book.objects.create(
                title="Fahrenheit 451",
                author="Ray Bradbury",
                published_date="1953-10-19",
                description="Books burn.",
                total_copies=1,
            ),
        )
        response = self.client.get(reverse("borrowed_books"))
        self.assertEqual(len(response.data), 2)