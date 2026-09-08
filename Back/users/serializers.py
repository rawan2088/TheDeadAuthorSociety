from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'books', 'joined_date']
        read_only_fields = ['id', 'is_admin', 'books', 'joined_date']