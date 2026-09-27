from django.urls import path
from . import views


urlpatterns = [
    # Borrowing & Management
    # should show borrowed books for current user, and post a new borrow record
    path('borrowed/', views.BorrowedBooksListAPIView.as_view(), name="borrowed_books"),
    path('borrowed/<int:pk>/return/', views.ReturnBookAPIView.as_view(), name="return_book"),
        # path('books/<int:id>/borrow/', views.borrow_book, name='borrow_book'),

]