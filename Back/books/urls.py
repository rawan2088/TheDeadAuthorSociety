from django.urls import path
from . import views


urlpatterns = [
    # # General Book List & Search
    path('books/', views.BookListAPIView.as_view(), name="books_list"), 

    # path('books/search/', book_search, name='book_search'),


    # # Specialized Lists
    # path('books/recent/', recent_books_view, name="recent_books"),
    # path('books/popular/', popular_books_view, name="popular_books"),
    
    # #! Category-Based
    path("categories/", views.CategoryAPIView.as_view(), name="book_by_category"), # get, post, update, delete
    # path("categories/<int:pk>/", views.book_by_category, name="book_by_category"),

    # #! Author-Based
    # path("books/authors/", views.book_by_author, name="book_by_author"),
    # path("books/authors/<str:author_name>/", views.book_by_author, name="book_by_author"),

    # # Individual Book Operations
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name="book_detail"), #get list of books, creates a book
    path('books/<int:pk>/comments/', views.CommentCreateAPIView.as_view(), name="book_comments"), # create a comment
    # path('books/<int:id>/borrow/', views.borrow_book, name='borrow_book'),
    # path('books/<int:id>/add-copy/', add_copy_view, name="add_copy"),

    # # Borrowing & Management
    # path('borrowed/', views.borrowed_books, name="borrowed_books"),
    # path('borrowed/<int:borrow_id>/return/', views.return_book, name="return_book"),
    

]