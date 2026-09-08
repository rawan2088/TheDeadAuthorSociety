from django.db import models

# from books.management.commands.seed import User
from books.models import Book
# from users.models import User
from django.conf import settings

# Create your models here.
#! each user can have up to 5 active borrowings, we will enforce that in the view
class BorrowedBook(models.Model):
    class StatusChoices(models.TextChoices):
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    
    
    # it is better to make a property of is_returned to check wether this specific one is returned or not rather than making another status field
    # why you ask?
    # because then you would have two entries with basically the same data with different formats
    # if by any mistake one is a thing and the other is another
    # then CHAOS 
    @property
    def is_returned(self):
        return self.return_date is not None
    
    # status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.BORROWED)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                # this one ensures that user can reborrow as long as he returned it at the first place
                condition=models.Q(return_date__isnull=True),
                name="one_active_borrowing_per_user_book"
            ),
            # a logical constraint, where the return date can never preceed the actual borrowing date
            models.CheckConstraint(
                # the q here preservses the order of the constraint, so it checks if the return date is null or if it is greater than or equal to the borrowed date
                condition=models.Q(return_date__isnull=True) | models.Q(return_date__gte=models.F('borrowed_date')),
                name='chk_return_after_borrow'
            )
        ]

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"