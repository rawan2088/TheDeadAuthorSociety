from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from All.models import Book, Comment, BorrowedBooks, Category
from django.utils import timezone
from datetime import datetime

User = get_user_model()

SEED_USERS = [
    {"firstName": "Admin", "lastName": "User", "username": "admin", "password": "admin123", "email": "admin@deadauthorsociety.com", "role": "admin"},
    {"firstName": "Rawan", "lastName": "Ahmed", "username": "Rawan", "password": "123456", "email": "rawan@gmail.com", "role": "admin"},
    {"firstName": "Roaa", "lastName": "AbdElFatah", "username": "Roaa", "password": "123456", "email": "roaa@gmail.com", "role": "user"},
    {"firstName": "Maryam", "lastName": "Ahmed", "username": "Maryam", "password": "123456", "email": "maryam@gmail.com", "role": "user"},
]

SEED_BOOKS = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "published_date": "1925-01-01",
        "category": "Classic Fiction",
        "description": "Published in 1925, The Great Gatsby is a classic piece of American fiction told from the perspective of Nick Carraway about the eponymous Jay Gatsby, set over a few months in 1922.",
        "image": "book_covers/book1.webp",
        "totalCopies": 5,
        "availableCopies": 5,
    },
    {
        "title": "To Kill A Mockingbird",
        "author": "Harper Lee",
        "published_date": "1960-01-01",
        "category": "Southern Gothic",
        "description": "Set in small-town Alabama, the novel chronicles the childhood of Scout and Jem Finch as their father Atticus defends a Black man falsely accused of rape.",
        "image": "book_covers/book2.jpg",
        "totalCopies": 4,
        "availableCopies": 4,
    },
    {
        "title": "Call It What You Want",
        "author": "Brigid Kemmerer",
        "published_date": "2023-01-01",
        "category": "Young Adult",
        "description": "When his dad is caught embezzling funds from half the town, Rob goes from popular lacrosse player to social pariah, while Maegan hides secrets of her own.",
        "image": "book_covers/book3.jpg",
        "totalCopies": 3,
        "availableCopies": 0,
    },
    {
        "title": "A Good Girl's Guide To Murder",
        "author": "Holly Jackson",
        "published_date": "2019-01-01",
        "category": "Mystery Thriller",
        "description": "Five years ago, schoolgirl Andie Bell was murdered by Sal Singh — or so everyone believes. Pippa Fitz-Amobi isn't convinced and starts digging for the truth.",
        "image": "book_covers/book4.jpg",
        "totalCopies": 6,
        "availableCopies": 6,
    },
    {
        "title": "Betting on You",
        "author": "Lynn Painter",
        "published_date": "2023-01-01",
        "category": "Romance",
        "description": "When seventeen-year-old Bailey starts a new job at a hotel waterpark, she runs into Charlie — an old acquaintance whose cynicism clashes with her careful temperament.",
        "image": "book_covers/book5.jpg",
        "totalCopies": 3,
        "availableCopies": 0,
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "published_date": "1813-01-01",
        "category": "Classical Romance",
        "description": "Jane Austen's much-adapted novel is famed for its witty, spirited heroine and sensational romances, with deft remarks on the triumphs and pitfalls of social convention.",
        "image": "book_covers/book6.jpg",
        "totalCopies": 5,
        "availableCopies": 5,
    },
    {
        "title": "Steal Like an Artist",
        "author": "Austin Kleon",
        "published_date": "2012-01-01",
        "category": "Self Help",
        "description": "A manifesto for the digital age — a guide with positive messages, illustrations, and exercises that puts readers directly in touch with their artistic side.",
        "image": "book_covers/book7.jpg",
        "totalCopies": 4,
        "availableCopies": 0,
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "published_date": "2019-01-01",
        "category": "Mystery Thriller",
        "description": "Alicia Berenson's life seems perfect until she shoots her husband five times in the face — and then never speaks another word.",
        "image": "book_covers/book8.jpg",
        "totalCopies": 5,
        "availableCopies": 5,
    },
    {
        "title": "Little Women",
        "author": "Louisa May Alcott",
        "published_date": "1868-01-01",
        "category": "Historical Fiction",
        "description": "Generations of readers have fallen in love with the March sisters — Jo, Beth, Meg, and Amy — united in devotion to each other during the Civil War era.",
        "image": "book_covers/book9.jpg",
        "totalCopies": 4,
        "availableCopies": 0,
    },
]

SEED_COMMENTS = [
    {"book_title": "The Great Gatsby", "username": "Roaa", "rating": 5, "content": "An absolute masterpiece. Highly recommend to everyone!", "date": "2024-01-15"},
    {"book_title": "The Great Gatsby", "username": "Rawan", "rating": 4, "content": "A great read, kept me engaged from start to finish.", "date": "2024-02-20"},
    {"book_title": "To Kill A Mockingbird", "username": "Roaa", "rating": 5, "content": "One of the most important books I have ever read.", "date": "2024-03-10"},
    {"book_title": "A Good Girl's Guide To Murder", "username": "Rawan", "rating": 5, "content": "Could not put it down. Finished it in one sitting!", "date": "2024-04-05"},
    {"book_title": "Pride and Prejudice", "username": "Roaa", "rating": 5, "content": "A timeless classic. Elizabeth Bennet is iconic.", "date": "2024-05-18"},
    {"book_title": "The Silent Patient", "username": "Rawan", "rating": 5, "content": "The twist at the end blew my mind completely.", "date": "2024-06-22"},
]

SEED_BORROWED = [
    {"username": "Rawan", "book_title": "Call It What You Want", "date": "2024-06-01"},
    {"username": "Rawan", "book_title": "Betting on You", "date": "2024-06-15"},
    {"username": "Roaa", "book_title": "Steal Like an Artist", "date": "2024-07-01"},
    {"username": "Roaa", "book_title": "Little Women", "date": "2024-07-10"},
]

class Command(BaseCommand):
    help = 'Seed the database with Users, Books, Comments, and Borrowed records'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Delete everything before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            Comment.objects.all().delete()
            BorrowedBooks.objects.all().delete()
            Book.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING('Cleared existing data.'))

        # 1. Seed Users
        for u_data in SEED_USERS:
            user, created = User.objects.get_or_create(
                username=u_data['username'],
                defaults={
                    'first_name': u_data['firstName'],
                    'last_name': u_data['lastName'],
                    'email': u_data['email'],
                    'is_admin': u_data['role'] == 'admin'
                }
            )
            if created:
                user.set_password(u_data['password'])
                user.save()
                self.stdout.write(f"User created: {user.username}")

        # 2. Seed Books
        for b_data in SEED_BOOKS:
            # Create/Get the Category first
            cat_name = b_data.pop('category')
            category_obj, _ = Category.objects.get_or_create(name=cat_name)
            
            book, created = Book.objects.get_or_create(
                title=b_data['title'],
                author=b_data['author'],
                defaults={**b_data, 'category': category_obj}
            )
            if created:
                self.stdout.write(f"Book created: {book.title}")

        # 3. Seed Comments
        for c_data in SEED_COMMENTS:
            try:
                user = User.objects.get(username=c_data['username'])
                book = Book.objects.get(title=c_data['book_title'])
                
                # Note: Comment model provided doesn't have created_at. 
                # If you add it later, you can add it to the defaults below.
                Comment.objects.get_or_create(
                    userId=user,
                    bookId=book,
                    content=c_data['content'],
                    defaults={
                        'username': user.username,
                        'rating': c_data['rating'],
                    }
                )
            except (User.DoesNotExist, Book.DoesNotExist):
                continue

        # 4. Seed Borrowed Records
        for br_data in SEED_BORROWED:
            try:
                user = User.objects.get(username=br_data['username'])
                book = Book.objects.get(title=br_data['book_title'])
                
                # Date parsing for the borrowed_date
                b_date = datetime.strptime(br_data['date'], "%Y-%m-%d").date()
                
                BorrowedBooks.objects.get_or_create(
                    userId=user,
                    bookId=book,
                    # Note: models has auto_now_add=True, so manual dates 
                    # might be ignored unless auto_now_add is removed.
                    defaults={'borrowed_date': b_date}
                )
            except (User.DoesNotExist, Book.DoesNotExist):
                continue

        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))