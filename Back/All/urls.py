from django.urls import path
from .views import books_view, book_detail_view, add_copy_view

urlpatterns = [
    path('', books_view),
    path('<int:id>/', book_detail_view),
    path('<int:id>/add-copy/', add_copy_view)
]