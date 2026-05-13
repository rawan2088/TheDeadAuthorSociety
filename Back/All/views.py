import json
# Returns data formatted as json instead of returning an HTML page. This is what APIs use
from django.http import JsonResponse
# CSRF is protection that blocks certain requests
from django.views.decorators.csrf import csrf_exempt
# this is how we access the database table
from django.db import transaction
from django.db.models import F, Q, Count
from django.utils import timezone
from django.shortcuts import render
from .models import Book, BorrowedBooks, Comment, Category

# helper funcitons
def get_image_url(request, book):
    if book.image:
        return request.build_absolute_uri(book.image.url)
    return ''

def serialize_book(request, book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category.name if book.category else None,
        'description': book.description,
        'totalCopies': book.totalCopies,
        'availableCopies': book.availableCopies,
        'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
        'image': get_image_url(request, book),
    }

# --- BOOK VIEWS ---

@csrf_exempt
def books_view(request):
    if request.method == "GET":
        books = Book.objects.all()
        data = [serialize_book(request, b) for b in books]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_admin:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        data = json.loads(request.body)
        
        # Resolve category object if provided
        cat_name = data.get('category')
        category_obj = None
        if cat_name:
            category_obj, _ = Category.objects.get_or_create(name=cat_name)

        Book.objects.create(
            title=data.get('title', ''),
            author=data.get('author', ''),
            category=category_obj,
            description=data.get('description', ''),
            totalCopies=data.get('totalCopies', 1),
            availableCopies=data.get('totalCopies', 1),
            published_date=data.get('published_date', '1900-01-01'),
        )
        return JsonResponse({'message': 'Book created'}, status=201)

@csrf_exempt
def book_detail_view(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(serialize_book(request, book))
    
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    if request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        book.totalCopies = data.get('totalCopies', book.totalCopies)
        book.availableCopies = data.get('availableCopies', book.availableCopies)
        book.save()
        return JsonResponse({'message': 'Book updated'}, status=200)
    
    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book deleted'}, status=200)

@csrf_exempt
def add_copy_view(request, id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    if request.method == 'POST':
        try:
            book = Book.objects.get(id=id)
            book.totalCopies += 1
            book.availableCopies += 1
            book.save()
            return JsonResponse({'message': 'Copy added'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

# RECENT & POPULAR 

def recent_books_view(request):
    books = Book.objects.all().order_by('-id')[:10]
    data = [serialize_book(request, b) for b in books]
    return JsonResponse(data, safe=False)

def popular_books_view(request):
    books = Book.objects.annotate(borrow_count=Count('borrow_records')).order_by('-borrow_count')[:10]
    data = []
    for b in books:
        item = serialize_book(request, b)
        item['borrow_count'] = b.borrow_count
        data.append(item)
    return JsonResponse(data, safe=False)

# SEARCH & CATEGORY

@csrf_exempt
def book_search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'success': False, 'error': 'Query required'}, status=400)
    
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) | Q(category__name__icontains=query)
    )
    data = [serialize_book(request, b) for b in books]
    return JsonResponse({'success': True, 'results': data})

@csrf_exempt
def book_by_category(request, category_name):
    books = Book.objects.filter(category__name__iexact=category_name)
    data = [serialize_book(request, b) for b in books]
    return JsonResponse({'results': data}, status=200)

# BORROW & RETURN

@csrf_exempt
def borrow_book(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        with transaction.atomic():
            book = Book.objects.select_for_update().get(id=id)
            if book.availableCopies <= 0:
                return JsonResponse({'error': 'No copies available'}, status=400)
            
            if BorrowedBooks.objects.filter(userId=request.user, bookId=book, return_date__isnull=True).exists():
                return JsonResponse({'error': 'You already have this book'}, status=400)

            BorrowedBooks.objects.create(userId=request.user, bookId=book)
            book.availableCopies = F('availableCopies') - 1
            book.save()
        return JsonResponse({'message': 'Book borrowed successfully'}, status=201)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

def borrowed_books(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    records = BorrowedBooks.objects.filter(userId=request.user, return_date__isnull=True).select_related('bookId')
    data = []
    for r in records:
        data.append({
            'borrowId': r.id,
            'borrowDate': r.borrowed_date.strftime('%Y-%m-%d'),
            'book': serialize_book(request, r.bookId)
        })
    return JsonResponse({'borrowed': data}, safe=False)

@csrf_exempt
def return_book(request, borrow_id):
    if request.method != 'POST' or not request.user.is_authenticated:
        return JsonResponse({'error': 'Invalid request'}, status=401)
    try:
        with transaction.atomic():
            record = BorrowedBooks.objects.get(id=borrow_id, userId=request.user, return_date__isnull=True)
            record.return_date = timezone.now().date()
            record.save()
            
            book = record.bookId
            book.availableCopies = F('availableCopies') + 1
            book.save()
        return JsonResponse({'message': 'Book returned successfully'}, status=200)
    except BorrowedBooks.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)
    
# Add to All/views.py:
@csrf_exempt
def book_comments_view(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        comments = Comment.objects.filter(bookId=book)
        data = [{'username': c.username, 'rating': c.rating, 
                 'content': c.content} for c in comments]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login to post a comment.'}, status=401)
        body = json.loads(request.body)
        Comment.objects.create(
            userId=request.user,
            bookId=book,
            username=request.user.username,
            rating=body.get('rating', 5),
            content=body.get('content', ''),
        )
        return JsonResponse({'message': 'Comment added'}, status=201)

# --- PAGE RENDERING ---

def book_page(request): return render(request, 'book.html')
def borrowed_page(request): return render(request, 'Borrowed.html')
def search_page(request): return render(request, 'SearchPage.html')
def category_page(request): return render(request, 'CategoryPage.html')