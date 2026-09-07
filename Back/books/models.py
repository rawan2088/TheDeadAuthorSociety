from django.db import models
from django.conf import settings

# from users.models import User
# don't import users, but import settings and use
# settings.AUTH_USER_MODEL to avoid circular imports

# we can create new categories here, we only need the name really.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(
        upload_to='book_covers/', 
        default='book_covers/default.jpg', 
        blank=True, 
        null=True
    )
    
    # a book can belong to multiple categories
    #* there is something called thorough, which we can use with many to many relationships to make the intermediate table.
    #* to make this, we do the intermidiate table, then we add the entry of plural into each of the other two tables
    #*     books = models.ManyToManyField( Book, through="Borrowing", related_name="borrowers" )
    #* like this
    categories = models.ManyToManyField(
        Category, 
        #! you can't have ondelet or null in a manytomany field
        # null=True, 
        # on_delete=models.SET_NULL, 
        # this would do a books field for each category
        related_name='books',
    )
    
    #* borrowers
    #* we dont need to add the entry field borrowers here, it is already added since we make the related name in the user model
    #* django will automatically use it to make the reverse field here
    
    #* comments
    
    total_copies = models.PositiveIntegerField(default=1)
    
    
    # availableCopies = models.PositiveIntegerField(default=1)
    @property 
    def available_copies (self):
        # ! you cannot use a property in filter, because filter is calculated at the database level while the property is python level
        # return self.total_copies - self.borrowers.filter(is_returned = False).count() 
        return self.total_copies - self.borrowers.filter(returned_at__isnull = False).count() 
    #again get away from duplicated entries


    # # adds a property that shouldn't be violated
    # @property
    # def availableCopies(self):
    #     return self.totalCopies - self.borrowed_books.filter(return_date__isnull=True).count()
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    # username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"