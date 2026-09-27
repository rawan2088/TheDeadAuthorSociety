from rest_framework import serializers
from .models import Book, Comment, Category

from borrowed.serializers import BorrowedBookSerializer

# * ----- Serializers ------
# would be used like views for us 
# where you could have more than one serializer for a model, and you can use them in different views, or even in the same view, depending on what you want to do with the data
# you make serializers depending on the needed output data

# model serializers are inherted from normal seriazliazers, they assign serializer friendly fields to each of the model fields, and they also provide create and update methods for you, so you don't have to write them yourself
# . Reverse relationships are not included by default unless explicitly included as specified in the serializer relations documentation.


#  * ------ MethodSerializers --------
# there are serializerMethodField, which is a read-only field that gets its value by calling a method on the serializer class it is attached to. The method should be named get_<field_name> and should take the object being serialized as its only argument. This is useful for adding custom data to your serialized output that isn't directly tied to a model field.
# The value depends on something outside the model instance — the request (e.g. request.user), query params, serializer context, or view logic.
# It's serialization-specific and doesn't belong on the model (the model shouldn't know about HTTP requests).
# You need per-serializer variation — e.g. one serializer wants "active borrows only," another wants "all borrows," so the same underlying data needs different shaping depending on which serializer you're in.


# todo: have to handle the images, and the categories
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        


# we don't have to make a serializer for book list, in the view, we would use each single book serialzier and return a list of them
class BookSerializer(serializers.ModelSerializer):
    # this here is a landmine, this way you can't attach categories while making the book, which is a feature we need.
    
    categories_ids = serializers.PrimaryKeyRelatedField(source='categories', many=True, queryset=Category.objects.all(), write_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    is_available = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None)
    
    
    def get_is_available(self, obj):
        # obj.active_borrow_count comes from the .annotate() in the view —
        # falls back to a live count only if the queryset wasn't annotated
        available = getattr(obj, 'available_copies', None)
        if available is None:
            available = obj.total_copies - obj.borrow_records.filter(return_date__isnull=True).count()
        return available > 0
        
    class Meta:
        model = Book
        # already implicitly read only 
        fields = ['id', 'title', 'author', 'published_date', 'description', 'image', 'categories_ids', 'categories', 'is_available', 'avg_rating', 'date_added']
        # all is only valid for fields
        read_only_fields = ['id', 'title', 'author', 'published_date', 'description', 'image', 'categories', 'is_available', 'avg_rating','date_added']
        # read_only_fields = ['__all__'] // no
        # fields = ['__all__']
        
        
class AdminBookSerializer(serializers.ModelSerializer):
    # we can use a primary key related field, where it would only provide us with the primary keys of the categories
    
    
    # TEMP
    # categories = serializers.CharField()
    categories = CategorySerializer(many=True)
    
    avg_rating = serializers.ReadOnlyField()
    borrow_records = BorrowedBookSerializer(many=True, read_only=True)
    
    available_copies = serializers.IntegerField(read_only=True)
    # def get_available_copies(self, obj):
    #     # obj.active_borrow_count comes from the .annotate() in the view —
    #     # falls back to a live count only if the queryset wasn't annotated
    #     active = getattr(obj, 'active_borrow_count', None)
    #     if active is None:
    #         active = obj.borrow_records.filter(return_date__isnull=True).count()
    #     return obj.total_copies - active

    is_available = serializers.SerializerMethodField(read_only=True, default=True )
    def get_is_available(self, obj):
        available = getattr(obj, 'available_copies', None)
        if available is None:
            available = obj.total_copies - obj.borrow_records.filter(return_date__isnull=True).count()
        return available > 0
    
    
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
            'date_added',
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

class CommentCreateSerializer(serializers.ModelSerializer):
    # the user and book fields 

    class Meta:
        model = Comment
        fields = ['user', 'book', 'content', 'rating','created_at']
        read_only_fields = ['user', 'book', 'created_at']
        

class BookCategoryDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'description', 'image', 'avg_rating', 'date_added']
        read_only_fields = ['title', 'author', 'published_date', 'description', 'image', 'avg_rating', 'date_added']

        

class CategoryDetailSerializer(serializers.ModelSerializer):

    # if books is representing one book
    # book_author = serializers.CharField(source='books.author', read_only=True)
    
    books = BookCategoryDetailSerializer(many=True,read_only=True)
    # books = BookSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'books']