from django.urls import path
from . import views
from .views import (
    books_view, 
    book_detail_view, 
    add_copy_view, 
    book_comments_view, 
    recent_books_view, 
    popular_books_view
)

urlpatterns = [
    # General Book List & Search
    path('books/', books_view, name="books_list"),

    # Specialized Lists
    path('books/recent/', recent_books_view, name="recent_books"),
    path('books/popular/', popular_books_view, name="popular_books"),
    path("books/category/<str:category_name>/", views.book_by_category, name="book_by_category"),

    # Individual Book Operations
    path('books/<int:id>/', book_detail_view, name="book_detail"),
    path('books/<int:id>/comments/', book_comments_view, name="book_comments"),
    path('books/<int:id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:id>/add-copy/', add_copy_view, name="add_copy"),

    # Borrowing & Management
    path('borrowed/', views.borrowed_books, name="borrowed_books"),
    path('borrowed/<int:borrow_id>/return/', views.return_book, name="return_book"),
]