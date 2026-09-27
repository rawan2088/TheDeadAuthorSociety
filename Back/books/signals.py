from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from books.models import Book
from django.core.cache import cache


@receiver([post_delete, post_save], sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    print('clearing book cache')
    
    # clear the book cache
    cache.delete_pattern('*book_list*')