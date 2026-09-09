from django.contrib import admin
from .models import BorrowedBook

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'due_date', 'return_date')
    search_fields = ('book__title', 'user__username')
    list_filter = ('borrow_date', 'due_date', 'return_date')