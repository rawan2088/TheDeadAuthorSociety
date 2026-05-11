from django.urls import path
from .views import books_view, book_detail_view, add_copy_view,views

urlpatterns = [
    # GET /api/books/search/?q=...
    path("books/search/",                        views.book_search,     name="book_search"),

    # GET /api/books/category/<name>/
    path("books/category/<str:category_name>/",  views.book_by_category, name="book_by_category"),

    # GET /api/books/<id>/
    path("books/<int:book_id>/",                 views.book_detail,     name="book_detail"),

    # POST /api/books/<id>/borrow/
    path("books/<int:book_id>/borrow/",          views.borrow_book,     name="borrow_book"),

    # GET /api/borrowed/
    path("borrowed/",                            views.borrowed_books,  name="borrowed_books"),

    # POST /api/borrowed/<id>/return/
    path("borrowed/<int:borrow_id>/return/",     views.return_book,     name="return_book"),

    path('', books_view),
    path('<int:id>/', book_detail_view),
    path('<int:id>/add-copy/', add_copy_view)
]