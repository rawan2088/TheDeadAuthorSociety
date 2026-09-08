from rest_framework import serializers
from .models import Book, Comment, Category

from borrowed.serializers import BorrowedBookSerializer

# * serializers would be used like views for us 
# where you could have more than one serializer for a model, and you can use them in different views, or even in the same view, depending on what you want to do with the data
# you make serializers depending on the needed output data

# model serializers are inherted from normal seriazliazers, they assign serializer friendly fields to each of the model fields, and they also provide create and update methods for you, so you don't have to write them yourself
# . Reverse relationships are not included by default unless explicitly included as specified in the serializer relations documentation.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# we don't have to make a serializer for book list, in the view, we would use each single book serialzier and return a list of them
class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        # already implicitly read only 
        fields = ['id', 'title', 'author', 'published_date', 'description', 'image', 'categories', 'is_available', 'avg_rating']
        # all is only valid for fields
        # read_only_fields = ['id', 'title', 'author', 'published_date', 'description', 'image', 'categories', 'is_available', 'avg_rating']
        # read_only_fields = ['__all__'] // no
        # fields = ['__all__']
        
        
class AdminBookSerializer(serializers.ModelSerializer):
    # we can use a primary key related field, where it would only provide us with the primary keys of the categories
    categories = CategorySerializer(many=True)
    available_copies = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()
    borrow_records = BorrowedBookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'published_date',
            'description',
            'image',
            'categories',
            'avg_rating',
            'is_available',
            'total_copies',
            'available_copies',
            'borrow_records',  # Include the related BorrowedBook records
            
            # this one indicates that we want all fields of the model
            # execlud would do the same thing   
            # '__all__'
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    # the user and book fields 

    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'content', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'book', 'created_at'] 