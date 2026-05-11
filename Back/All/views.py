import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Book, BorrowedBooks


def book_to_dict(book):
    return {
        "id":              book.id,
        "title":           book.title,
        "author":          book.author,
        "published_date":  str(book.published_date),
        "category":        book.category,
        "description":     book.description,
        "image":           book.image.url if book.image else None,
        "totalCopies":     book.totalCopies,
        "availableCopies": book.availableCopies,
    }



def book_detail(request, book_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)
    return JsonResponse(book_to_dict(book))



def book_search(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"error": "Query parameter 'q' is required"}, status=400)

    books = Book.objects.filter(
        Q(title__icontains=q) |
        Q(author__icontains=q) |
        Q(category__icontains=q)
    )
    return JsonResponse({"results": [book_to_dict(b) for b in books]})



def book_by_category(request, category_name):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    books = Book.objects.filter(category__iexact=category_name)
    return JsonResponse({"results": [book_to_dict(b) for b in books]})



@csrf_exempt
def borrow_book(request, book_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    # Admins cannot borrow
    if request.user.is_admin:
        return JsonResponse({"error": "Admins cannot borrow books"}, status=403)

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    # Check availability
    if book.availableCopies <= 0:
        return JsonResponse({"error": "No copies available"}, status=400)

    # Check if user already has this book borrowed (and not returned)
    already = BorrowedBooks.objects.filter(
        userId=request.user,
        bookId=book,
        return_date__isnull=True
    ).exists()
    if already:
        return JsonResponse({"error": "You have already borrowed this book"}, status=400)

    # Create borrow record and decrement available copies
    BorrowedBooks.objects.create(userId=request.user, bookId=book)
    book.availableCopies -= 1
    book.save()

    return JsonResponse({
        "message": f'"{book.title}" borrowed successfully!',
        "availableCopies": book.availableCopies,
    }, status=201)



def borrowed_books(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    records = BorrowedBooks.objects.filter(
        userId=request.user
    ).select_related("bookId")

    data = []
    for record in records:
        data.append({
            "borrowId":    record.id,
            "borrowDate":  str(record.borrowed_date),
            "returnDate":  str(record.return_date) if record.return_date else None,
            "book":        book_to_dict(record.bookId),
        })

    return JsonResponse({"borrowed": data})



@csrf_exempt
def return_book(request, borrow_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        record = BorrowedBooks.objects.get(pk=borrow_id, userId=request.user)
    except BorrowedBooks.DoesNotExist:
        return JsonResponse({"error": "Borrow record not found"}, status=404)

    if record.return_date is not None:
        return JsonResponse({"error": "Book already returned"}, status=400)

    from django.utils import timezone
    record.return_date = timezone.now().date()
    record.save()

    # Give back the copy
    book = record.bookId
    book.availableCopies += 1
    book.save()

    return JsonResponse({"message": f'"{book.title}" returned successfully!'})
