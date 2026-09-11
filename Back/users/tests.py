# # Place at: users/tests.py (or wherever accounts/urls.py + views.py live)
# #
# # NOTE: these tests assume two fixes have been applied first (see chat):
# #   1. UserProfileAPIView.get_object() is overridden to return
# #      self.request.user, since the "users/me/" URL has no <pk> kwarg for
# #      the default RetrieveAPIView.get_object() to use.
# #   2. The url names in accounts/urls.py are de-duplicated, e.g.
# #         path('users/me/', ..., name='user_me')
# #         path('users/me/borrowed', ..., name='user_me_borrowed')
# #      Both currently share name='me', which makes reverse('me') resolve
# #      to whichever pattern the resolver happens to pick -- unreliable.

# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase

# from books.models import Book
# from borrowed.models import BorrowedBook

# User = get_user_model()


# class UserProfileAPITests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="dana", password="pass123", email="dana@example.test"
#         )

#     def test_profile_requires_authentication(self):
#         response = self.client.get(reverse("user_me"))
#         # much more readable
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_authenticated_user_sees_own_profile(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(reverse("user_me"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["username"], "dana")

#     def test_profile_does_not_expose_password(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(reverse("user_me"))
#         self.assertNotIn("password", response.data)


# class UserBorrowedListAPITests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="erin", password="pass123")
#         self.other_user = User.objects.create_user(username="frank", password="pass123")

#         self.own_book = Book.objects.create(
#             title="Neuromancer",
#             author="William Gibson",
#             published_date="1984-07-01",
#             description="Cyberpunk origin story.",
#             total_copies=2,
#         )
#         self.other_book = Book.objects.create(
#             title="Snow Crash",
#             author="Neal Stephenson",
#             published_date="1992-06-01",
#             description="Pizza delivery, but make it cyberpunk.",
#             total_copies=2,
#         )

#         self.own_record = BorrowedBook.objects.create(user=self.user, book=self.own_book)
#         BorrowedBook.objects.create(user=self.other_user, book=self.other_book)

#     def test_requires_authentication(self):
#         response = self.client.get(reverse("user_me_borrowed"))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_only_returns_own_borrow_records(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(reverse("user_me_borrowed"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["id"], self.own_record.id)

#     def test_does_not_leak_other_users_records(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(reverse("user_me_borrowed"))
#         book_titles = [r["book"] for r in response.data]
#         self.assertNotIn(self.other_book.id, book_titles)