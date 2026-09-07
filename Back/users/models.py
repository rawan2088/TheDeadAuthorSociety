from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# this resets everything in the database, we would do this here because we deleted the profile model
# python manage.py migrate authentication zero


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    #* related_name is the name Django gives you for accessing the related objects from the other side of a relationship.
    # for any many to many relationship, django do an intermediate table for you automatically
    # if you already have one that you want to use, you use the through argument to specify the model that should be used as the intermediate table.
    books = models.ManyToManyField(
        'books.Book',
        through='borrowed.BorrowedBook',
        related_name='borrowers'
    )

    def __str__(self):
        return self.username
