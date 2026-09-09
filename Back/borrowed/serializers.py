from rest_framework import serializers
from .models import BorrowedBook

class BorrowedBookSerializer(serializers.ModelSerializer):
    # here, we use some of these fields inside the DRF validation phase
    # but we also make it readonly
    # so the website itself would not provide us with these data at that point, so we need to make the user here explictly 
    # this is called unique_together problem
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    # ! A golden rule of thump, if the data is not required to be changed manually, never make it not read only
    # the return date here should be readonly to not allow the user to manually change it, it should be changed only when the user returns the book, and that should be done in the view
    # return_date = serializers.DateField(read_only=True)
    
    # you cannot put a property inside the fields list
    is_returned = serializers.ReadOnlyField()
    
    class Meta:
        model = BorrowedBook
        fields = ['id', 'user','book', 'borrow_date','due_date', 'return_date', 'is_returned']
        read_only_fields = ['id', 'book', 'borrow_date','due_date', 'return_date']  # 'user' is also read-only, but we set it explicitly above

