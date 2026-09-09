from django.urls import path
from . import views


urlpatterns = [
   
    # Borrowing & Management
    path('borrowed-books/', views.BorrowedBooksListAPIView.as_view(), name="borrowed_books"),
    # path('borrowed/<int:borrow_id>/return/', views.return_book, name="return_book"),
    

]