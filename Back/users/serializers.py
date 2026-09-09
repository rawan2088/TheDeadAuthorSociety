from rest_framework import serializers
from .models import User
from borrowed.serializers import BorrowedBookSerializer

# todo: can add a wishlist
# todo: a page only for borrowed books
class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'borrowed_books', 'date_joined']
        read_only_fields = ['id', 'is_admin', 'borrowed_books', 'date_joined']