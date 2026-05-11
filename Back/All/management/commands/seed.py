# All/management/commands/seed.py
from django.core.management.base import BaseCommand
from All.models import Book
        
# guyys, run 
# python manage.py seed
# i made this to populate the backend

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


class Command(BaseCommand):
    help = 'Seed the database with initial book data'

    def add_arguments(self, parser):
        # Optional flag: python manage.py seed --clear
        # Deletes all books first before re-seeding
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing books before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Book.objects.count()
            Book.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing books.'))

        created = 0
        skipped = 0

        for data in SEED_BOOKS:
            # Won't create duplicates if you run it twice —
            # checks by title + author before inserting
            book, was_created = Book.objects.get_or_create(
                title=data['title'],
                author=data['author'],
                defaults={
                    'published_date':  data['published_date'],
                    'category':        data['category'],
                    'description':     data['description'],
                    'image':           data['image'],
                    'totalCopies':     data['totalCopies'],
                    'availableCopies': data['availableCopies'],
                }
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Created: {book.title}')
            else:
                skipped += 1
                self.stdout.write(f'  Skipped (already exists): {book.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} books created, {skipped} skipped.'
        ))

