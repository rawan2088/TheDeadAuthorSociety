from django.urls import path
from . import views
from .views import books_view, book_detail_view, add_copy_view
from .views import book_comments_view, recent_books_view, popular_books_view

urlpatterns = [
    # GET /api/books/search/?q=...
    # path("books/search/", views.book_search, name="book_search"),

    # GET /api/books/category/<name>/
    # path("books/category/<str:category_name>/", views.book_by_category, name="book_by_category"),

    path('books/', books_view),
    path('books/<int:id>/', book_detail_view),
    path('books/<int:id>/add-copy/', add_copy_view),

    # POST /api/books/<id>/borrow/
    # path("books/<int:book_id>/borrow/", views.borrow_book, name="borrow_book"),

    # GET /api/borrowed/
    # path("borrowed/", views.borrowed_books, name="borrowed_books"),

    # POST /api/borrowed/<id>/return/
    # path("borrowed/<int:borrow_id>/return/", views.return_book, name="return_book"),


    # recent/ popular/ <int:id>/comments/
    path('books/recent/',            recent_books_view),
    path('books/popular/',           popular_books_view),
    path('books/<int:id>/comments/', book_comments_view),
]