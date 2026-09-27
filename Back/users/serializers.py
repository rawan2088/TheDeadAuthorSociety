from rest_framework import serializers
from .models import User
from borrowed.serializers import BorrowedBookSerializer

from django.contrib.auth.password_validation import validate_password

# todo: can add a wishlist
# todo: a page only for borrowed books
class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'borrowed_books', 'date_joined']
        read_only_fields = ['id', 'is_admin', 'borrowed_books', 'date_joined']
        
class UserSignupSerializer(serializers.ModelSerializer):
    # default validators to validate the password, instead of validate_password field
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        
        return User.objects.create_user(**validated_data)
        #! this is a very big problem, it stores plain text
        # return super().create(validated_data)
    class Meta:
        model = User
        fields = ['username', 'email', 'is_admin', 'password', 'confirm_password', 'date_joined']
        read_only_fields = ['date_joined']