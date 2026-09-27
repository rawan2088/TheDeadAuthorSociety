from django.shortcuts import render
from rest_framework import generics
from .serializers import BorrowedBookSerializer
from .models import BorrowedBook
from books.models import Book

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError, transaction

from django.utils import timezone

from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers




class BorrowedBooksListAPIView(generics.ListAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60* 15, key_prefix='borrowed_list'))
    @method_decorator(vary_on_headers("Authentication")) # this becomes based on the authentication header, that changes with each new access key generated in jwt
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)
    
    
# !! made it in the books url
# MAX_ACTIVE_RECORDS = 5
# # use APIView since you don't use the mixins
# class BorrowBookAPIView(APIView):
#     queryset = BorrowedBook.objects.all()
#     serializer_class = BorrowedBookSerializer
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, pk):
#         book = get_object_or_404(Book, pk=pk)
#         user = request.user
        
#         # ORM
#         current_active_records = BorrowedBook.objects.filter(
#             user=user,
#             return_date__isnull=True,
#         ).count()
        
#         if current_active_records >= MAX_ACTIVE_RECORDS:
#             return Response({'detail': 'You can not borrow more than 5 books at a time'}, status=status.HTTP_400_BAD_REQUEST)
        
#         available_copies = book.total_copies -  book.borrow_records.filter(return_date__isnull=True).count()
        
#         if available_copies <= 0:
#             return Response({'detail': 'This book is currently out of stock, retry again later this week.'},status=status.HTTP_400_BAD_REQUEST )
        
#         try:
#             # todo: learn transactions
#             with transaction.atomic():
#                 record = BorrowedBook.objects.create(user=user, book=book)
#         except IntegrityError:
#             return Response(
#                 {'detail': 'You already have this book borrowed.'}, status=400
#             )

#         return Response(BorrowedBookSerializer(record).data, status=201)
    
    
# since i am triggiring an action not returning an updated representation of the resource
class ReturnBookAPIView(APIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        record = get_object_or_404(BorrowedBook, pk=pk, user=request.user, return_date__isnull=True)
        
        # if record.return_date != None:
            # return Response({'detail: You already returned this book'})
            
        record.return_date = timezone.now().date()
        record.save()
        return Response(BorrowedBookSerializer(record).data, status=200)
        