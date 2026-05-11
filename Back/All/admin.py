from django.contrib import admin
from .models import Book, BorrowedBooks, Comment, User

admin.site.register(Book)
admin.site.register(BorrowedBooks)
admin.site.register(Comment)
admin.site.register(User)