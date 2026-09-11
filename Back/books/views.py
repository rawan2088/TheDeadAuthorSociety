import json
# Returns data formatted as json instead of returning an HTML page. This is what APIs use
from django.http import JsonResponse
# CSRF is protection that blocks certain requests
from django.views.decorators.csrf import csrf_exempt
# this is how we access the database table
from django.db import transaction
from django.db.models import F, Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from .models import Book, Comment, Category

from django.http import JsonResponse
from .serializers import BookSerializer, AdminBookSerializer, CommentSerializer, CategorySerializer, CommentCreateSerializer
from .models import Book, Comment, Category

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from rest_framework.views import APIView


# # helper funcitons
# def get_image_url(request, book):
#     if book.image:
#         return request.build_absolute_uri(book.image.url)
#     return ''



# ------- Class based Views --------

# -- Book views --

AnnotatedBooks= Book.objects.all().annotate(available_copies=F('total_copies') - Count('borrow_records', filter=Q(borrow_records__return_date__isnull=True))).prefetch_related('categories', 'comments', 'borrow_records')


# uses the list mixin and create mixin
# * views all books for everyone, and creates a new book if admin
class BookListAPIView(generics.ListCreateAPIView ):
    queryset = Book.objects.all().annotate(available_copies=F('total_copies') - Count('borrow_records', filter=Q(borrow_records__return_date__isnull=True))).prefetch_related('categories', 'comments', 'borrow_records')
    serializer_class = AdminBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated or not request.user.is_admin:
    #         return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
    #     return super().post(request, *args, **kwargs)
    
        
    
    
# start learning permissions here, there are three different views for a book details page
# -- Guest--
# would  view the basic book details and comments of other people only

# -- User --
# I should keep the borrowing btn available but with a warning sign if the user is not authenticated

# -- Admin --
# added info of available books, and total
# and can edit or delete a book

# there are two layers for this, first in the frontend we wouldn't show these data at all
# but here, even if the request happens we would not allow it

# retrieve a book, edit a book, delete a book

# annotation happens in the query set and it is far more efficint than property
# AnnotatedBook = Book.objects.annotate(available_copies blablabla=Count('borrow_records', filter=Q(borrow_records__return_date__isnull=True))).prefetch_related('categories', 'comments', 'borrow_records')

# * views the book for everyone, with extra details for admin.
class BookDetailAPIView(APIView):
    # queryset = get_object_or_404(Book, id=pk) dont need to do it, takes the object auto
    
    
    def get(self, request, id):
        # annotation doesn't work on single instances, it works on querysets
        book = get_object_or_404(AnnotatedBooks, id=id)
        
        if not request.user.is_admin:
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        serializer = AdminBookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def put(self, request):
    #     data = json.loads(request.body)
    #     serializer = Ad
    #     return JsonResponse({'message': 'Book updated'}, status=200)
        
    # def delete(self, request):
    #     book.delete()
    #     return JsonResponse({'message': 'Book deleted'}, status=200)
    

# * views all comments for a book, 
class CommentCreateAPIView(generics.ListCreateAPIView):
    # should be added
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
    # * ------ Both are valid ways to set the authentication to only get unless authenticated
        #** permission_classes = [IsAuthenticatedOrReadOnly]
    
    #* the ultimate way to set customized permissions
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
            
        return super().get_permissions()
    
    # * third way
        # def post(self, request, *args, **kwargs):
        #     if not request.user.is_authenticated:
        #         return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        #     return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super.get_queryset()
        
        # both are valid, but the second indicates the FK
        # return Comment.objects.filter(book__id = self.kwargs['pk'])
        return qs.filter(book_id = self.kwargs['pk'])
    
    
    def perform_create(self, serializer):
        # if you want to use book = , you have to pass a book object.
        # but django gives you the ability to do it using book_id to only pass the id
        serializer.save(user=self.request.user, book_id=self.kwargs['pk'])

    # if request.method == 'GET':
    #     comments = Comment.objects.filter(bookId=book)
    #     data = [{'username': c.username, 'rating': c.rating, 
    #              'content': c.content} for c in comments]
    #     return JsonResponse(data, safe=False)
    

class CategoryAPIView(APIView):
    queryset = Category.objects.all()
    serializer = CategorySerializer


# --- BOOK VIEWS ---


# @csrf_exempt
# def add_copy_view(request, id):
#     if not request.user.is_authenticated or not request.user.is_admin:
#         return JsonResponse({'error': 'Not authorized'}, status=403)
#     if request.method == 'POST':
#         try:
#             book = Book.objects.get(id=id)
#             book.totalCopies += 1
#             book.availableCopies += 1
#             book.save()
#             return JsonResponse({'message': 'Copy added'}, status=200)
#         except Book.DoesNotExist:
#             return JsonResponse({'error': 'Book not found'}, status=404)

# #-------- RECENT & POPULAR 

# def recent_books_view(request):
#     books = Book.objects.all().order_by('-id')[:10]
#     data = [serialize_book(request, b) for b in books]
#     return JsonResponse(data, safe=False)

# def popular_books_view(request):
#     books = Book.objects.annotate(borrow_count=Count('borrow_records')).order_by('-borrow_count')[:10]
#     data = []
#     for b in books:
#         item = serialize_book(request, b)
#         item['borrow_count'] = b.borrow_count
#         data.append(item)
#     return JsonResponse(data, safe=False)

# #--------------- SEARCH & CATEGORY

# @csrf_exempt
# def book_search(request):
#     query = request.GET.get('q', '').strip()
#     if not query:
#         return JsonResponse({'success': False, 'error': 'Query required'}, status=400)
    
#     books = Book.objects.filter(
#         Q(title__icontains=query) | Q(author__icontains=query) | Q(category__name__icontains=query)
#     )
#     data = [serialize_book(request, b) for b in books]
#     return JsonResponse({'success': True, 'results': data})

# @csrf_exempt
# def book_by_category(request, category_name):
#     books = Book.objects.filter(category__name__iexact=category_name)
#     data = [serialize_book(request, b) for b in books]
#     return JsonResponse({'results': data}, status=200)

# #--------------- BORROW & RETURN

# @csrf_exempt
# def borrow_book(request, id):
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'Authentication required'}, status=401)
#     try:
#         with transaction.atomic():
#             book = Book.objects.select_for_update().get(id=id)
#             if book.availableCopies <= 0:
#                 return JsonResponse({'error': 'No copies available'}, status=400)
            
#             if BorrowedBook.objects.filter(userId=request.user, bookId=book, return_date__isnull=True).exists():
#                 return JsonResponse({'error': 'You already have this book'}, status=400)

#             BorrowedBook.objects.create(userId=request.user, bookId=book)
#             book.availableCopies = F('availableCopies') - 1
#             book.save()
#         return JsonResponse({'message': 'Book borrowed successfully'}, status=201)
#     except Book.DoesNotExist:
#         return JsonResponse({'error': 'Book not found'}, status=404)

# def borrowed_books(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'Authentication required'}, status=401)
    
#     records = BorrowedBook.objects.filter(userId=request.user, return_date__isnull=True).select_related('bookId')
#     data = []
#     for r in records:
#         data.append({
#             'borrowId': r.id,
#             'borrowDate': r.borrow_date.strftime('%Y-%m-%d'),
#             'book': serialize_book(request, r.bookId)
#         })
#     return JsonResponse({'borrowed': data}, safe=False)

# @csrf_exempt
# def return_book(request, borrow_id):
#     if request.method != 'POST' or not request.user.is_authenticated:
#         return JsonResponse({'error': 'Invalid request'}, status=401)
#     try:
#         with transaction.atomic():
#             record = BorrowedBook.objects.get(id=borrow_id, userId=request.user, return_date__isnull=True)
#             record.return_date = timezone.now().date()
#             record.save()
            
#             book = record.bookId
#             book.availableCopies = F('availableCopies') + 1
#             book.save()
#         return JsonResponse({'message': 'Book returned successfully'}, status=200)
#     except BorrowedBook.DoesNotExist:
#         return JsonResponse({'error': 'Record not found'}, status=404)
    


# # --- PAGE RENDERING ---

# def book_page(request): return render(request, 'book.html')
# def borrowed_page(request): return render(request, 'Borrowed.html')
# def search_page(request): return render(request, 'SearchPage.html')
# def category_page(request): return render(request, 'CategoryPage.html')