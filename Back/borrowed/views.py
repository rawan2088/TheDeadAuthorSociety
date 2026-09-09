from django.shortcuts import render
from rest_framework import generics
from .serializers import BorrowedBookSerializer
from .models import BorrowedBook

class BorrowedBooksListAPIView(generics.ListAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer