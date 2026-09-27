from django.contrib import admin
from .models import Book, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # can't add categoris bec it is manytomany
    list_display = ('title', 'author', 'published_date', 'id')
    search_fields = ('title', 'author', 'id', 'categories__name')
    list_filter = ('categories', 'published_date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'content', 'created_at')
    search_fields = ('book__title', 'user__username', 'content')
    list_filter = ('created_at',) 
    
# @admin.register registers the class automatically

