import json
# Returns data formatted as json instead of returning an HTML page. This is what APIs use
from django.http import JsonResponse
# CSRF is protection that blocks certain requests
from django.views.decorators.csrf import csrf_exempt
# this is how we access the database table
from .models import Book, Comment, BorrowedBooks
from django.db.models import Count
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

def get_image_url(request, book):
    if book.image:
        return request.build_absolute_uri(book.image.url)
        # Returns something like: http://127.0.0.1:8000/media/book_covers/cover.jpg
    return ''  #default

@csrf_exempt
def books_view (request): # recieve HTTP request
    # GET retuens all books
    if request.method == "GET":
        # No Authorization needed. All user should view all books
        books = Book.objects.all()
        data = []
        for book in books:
            data.append({
    'id': book.id,
    'title': book.title,
    'author': book.author,
    'category': book.category,
    'description': book.description,
    'totalCopies': book.totalCopies,
    'availableCopies': book.availableCopies,
    'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
    'image': get_image_url(request, book),
            })
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        # Authorization check
        if not request.user.is_authenticated or not request.user.is_admin:
            return JsonResponse({'error': 'Not authorized'}, status=403)  # 403 Forbidden
        data = json.loads(request.body)
        title = data.get('title', '')
        author = data.get('author', '')
        category = data.get('category', '')
        description = data.get('description', '')
        totalCopies = data.get('totalCopies', '')
        published_date = data.get('published_date', '1900-01-01') # Default is obviously fake
        image = data.get('image', '')
        Book.objects.create(
            title = title,
            author= author,
            category= category,
            description= description,
            totalCopies= totalCopies,
            availableCopies= totalCopies, # Same as total Copies at creation
            published_date= published_date,
            image= image,
        )
        return JsonResponse({'message': 'Book created'}, status=201) # 201 means "created" in HTTP

# different function because PUT and DELETE have different URL
@csrf_exempt
def book_detail_view (request, id):
    
    # first check wether the book exists or not
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404) # 404 not found
    
    #then if 
    # we must first be sure that the check is when put and delete
    if request.method == 'GET':
        return JsonResponse({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'description': book.description,
                'totalCopies': book.totalCopies,
                'availableCopies': book.availableCopies,
                'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
                'image': get_image_url(request, book),});
    
    
    #Authorization check
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Not authorized'}, status=403)  # 403 Forbidden
    # first id is the field name in the DB. second id is the variable from the URL
    if request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.category = data.get('category', book.category)
        book.description = data.get('description', book.description)
        book.totalCopies = data.get('totalCopies', book.totalCopies)
        book.availableCopies = data.get('availableCopies', book.availableCopies)
        book.published_date = data.get('published_date', book.published_date)
        book.image = data.get('image', book.image)
        book.save()
        return JsonResponse({'message': 'Book updated'}, status=200)
    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book deleted'}, status=200) #200 OK

    # different function because this POST has different URL(adds copies)


@csrf_exempt
def add_copy_view (request, id):
    #Authorization check
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Not authorized'}, status=403)  # 403 Forbidden
    if request.method == 'POST':
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)  # 404 not found

        book.totalCopies += 1
        book.availableCopies += 1
        book.save()
        return  JsonResponse({'message': 'Copy added'}, status=200) #200 OK




@csrf_exempt
def book_comments_view(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        comments = Comment.objects.filter(bookId=book)
        data = []
        for comment in comments:
            data.append({
                'id':         comment.id,
                'username':   comment.username,
                'rating':     comment.rating,
                'content':    comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        data = json.loads(request.body)
        Comment.objects.create(
            userId=request.user,
            bookId=book,
            username=request.user.username,
            rating=data.get('rating', ''),
            content=data.get('content', ''),
        )
        return JsonResponse({'message': 'Comment added'}, status=201)


def recent_books_view(request):
    if request.method == 'GET':
        books = Book.objects.all().order_by('-id')[:10]
        data = []
        for book in books:
            data.append({
                'id':       book.id,
                'title':    book.title,
                'author':   book.author,
                'category': book.category,
                'image':    get_image_url(request, book),
            })
        return JsonResponse(data, safe=False)


def popular_books_view(request):
    if request.method == 'GET':
        books = Book.objects.annotate(
            borrow_count=Count('borrows')
        ).order_by('-borrow_count')[:10]
        data = []
        for book in books:
            data.append({
                'id':           book.id,
                'title':        book.title,
                'author':       book.author,
                'category':     book.category,
                'image':        get_image_url(request, book),
                'borrow_count': book.borrow_count,
            })
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def borrow_book(request, id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
           return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            with transaction.atomic():
                # Select_for_update prevents race conditions
                book = Book.objects.select_for_update().get(id=id)

                if book.availableCopies <= 0:
                    return JsonResponse({'error': 'No copies available'}, status=400)

                # Check if user already has an active borrow for this specific book
                already_borrowed = BorrowedBooks.objects.filter(
                    userId=request.user,
                    bookId=book,
                    return_date__isnull=True
                ).exists()

                if already_borrowed:
                    return JsonResponse({'error': 'You already have this book'}, status=400)

                # Create borrow record
                BorrowedBooks.objects.create(
                    userId=request.user,
                    bookId=book
                )

                # Decrement available copies
                book.availableCopies = F('availableCopies') - 1
                book.save()

            return JsonResponse({'message': 'Book borrowed successfully'}, status=201)

        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

def borrowed_books(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
           return JsonResponse({'error': 'Authentication required'}, status=401)

        # Get only active borrows (not yet returned)
        borrowed_records = BorrowedBooks.objects.filter(
            userId=request.user,
            return_date__isnull=True
        ).select_related('bookId')

        data = []
        for record in borrowed_records:
            data.append({
                'borrowId': record.id,
                'borrowDate': record.borrowed_date.strftime('%Y-%m-%d'),
                'book': {
                    'id': record.bookId.id,
                    'title': record.bookId.title,
                    'author': record.bookId.author,
                    'image': get_image_url(request, record.bookId),
                }
            })

        return JsonResponse({'borrowed': data}, safe=False)

@csrf_exempt
def return_book(request, borrow_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if not request.user.is_authenticated:
       return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        with transaction.atomic():
            borrow_record = BorrowedBooks.objects.get(
                id=borrow_id,
                userId=request.user,
                return_date__isnull=True
            )
            borrow_record.return_date = timezone.now().date()
            borrow_record.save()

            book = borrow_record.bookId
            book.availableCopies = F('availableCopies') + 1
            book.save()

        return JsonResponse({'message': 'Book returned successfully'}, status=200)

    except BorrowedBooks.DoesNotExist:
        return JsonResponse({'error': 'Active borrow record not found'}, status=404)
