from django.db import models
# to import the default user model
from django.contrib.auth.models import AbstractUser

# id is default in django
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    # i want to deal with this in the future
    image = models.ImageField(upload_to='book_covers/')
    totalCopies = models.IntegerField()
    availableCopies = models.IntegerField()
    

class BorrowedBooks(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    
class Comment (models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    rating = models.IntegerField() # 1 to 5
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)