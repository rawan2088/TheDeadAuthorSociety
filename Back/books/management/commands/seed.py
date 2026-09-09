"""
Management command to seed the database with randomized test data.

Place this file at: books/management/commands/seed_data.py
(create the management/ and commands/ folders with empty __init__.py files
if they don't exist yet)

Usage:
    python manage.py seed_data
    python manage.py seed_data --books 1000 --users 200
    python manage.py seed_data --flush   # wipes seeded data first
"""
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from books.models import Book, Category, Comment
from borrowed.models import BorrowedBook

from django.contrib.auth import get_user_model

User = get_user_model()

# ---- small local word banks, no external deps (no Faker needed) ----

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "David", "Elizabeth", "Ahmed", "Fatima", "Omar", "Layla",
    "Youssef", "Mariam", "Karim", "Nour", "Hana", "Sami", "Liam", "Olivia",
    "Noah", "Emma", "Ava", "Sophia", "Lucas", "Mia", "Ethan", "Zainab",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hassan", "Ibrahim", "Mansour",
    "Farouk", "Adel", "Salem", "Khalil", "Nasser", "Aziz", "Rashid",
]

TITLE_WORDS_A = [
    "The Silent", "Shadows of", "Beyond the", "Whispers in", "The Last",
    "Echoes of", "The Hidden", "A Song of", "The Broken", "Rise of",
    "The Forgotten", "Journey to", "The Secret", "Tales of", "The Lost",
]

TITLE_WORDS_B = [
    "Kingdom", "Storm", "River", "Empire", "Garden", "Ocean", "Mountain",
    "City", "Star", "Forest", "Desert", "Winter", "Flame", "Horizon",
    "Void", "Legacy", "Dawn", "Path", "Prophecy", "Realm",
]

CATEGORY_NAMES = [
    "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery",
    "Thriller", "Romance", "Horror", "Biography", "History", "Poetry",
    "Self-Help", "Science", "Technology", "Philosophy", "Psychology",
    "Business", "Travel", "Cooking", "Art", "Religion", "Politics",
    "Children", "Young Adult", "Classic Literature", "Drama", "Comics",
    "Economics", "Health", "Education",
]

COMMENT_SNIPPETS = [
    "Really enjoyed this one, couldn't put it down.",
    "Decent read but the pacing felt off in the middle.",
    "One of the best books I've read this year.",
    "Not really my genre, but the writing was solid.",
    "The ending felt rushed compared to the setup.",
    "A classic for a reason. Highly recommend.",
    "Interesting premise, mediocre execution.",
    "Loved the characters, hated the plot twists.",
    "Would read again. Great for a weekend.",
    "Overhyped in my opinion, but still worth a read.",
]


FAR_FUTURE_PLACEHOLDER = timezone.datetime(9999, 1, 1).date()


def random_date(start_year=1950, end_year=2023):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return timezone.datetime(year, month, day).date()


class Command(BaseCommand):
    help = "Seed the database with randomized books/users/comments/borrow records for load testing."

    def add_arguments(self, parser):
        parser.add_argument("--books", type=int, default=1000)
        parser.add_argument("--users", type=int, default=150)
        parser.add_argument("--comments-per-book", type=int, default=3)
        parser.add_argument("--borrow-records", type=int, default=1500)
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete previously seeded data (matching by username/title prefix) before seeding.",
        )

    def handle(self, *args, **options):
        n_books = options["books"]
        n_users = options["users"]
        comments_per_book = options["comments_per_book"]
        n_borrow_records = options["borrow_records"]

        if options["flush"]:
            self.stdout.write("Flushing previously seeded data...")
            Comment.objects.filter(user__username__startswith="seeduser_").delete()
            BorrowedBook.objects.filter(user__username__startswith="seeduser_").delete()
            Book.objects.filter(title__startswith="[seed]").delete()
            User.objects.filter(username__startswith="seeduser_").delete()
            Category.objects.filter(name__startswith="[seed] ").delete()

        with transaction.atomic():
            categories = self._seed_categories()
            users = self._seed_users(n_users)
            books = self._seed_books(n_books, categories)
            self._seed_comments(books, users, comments_per_book)
            self._seed_borrow_records(books, users, n_borrow_records)

        self.stdout.write(self.style.SUCCESS(
            f"Done. {len(users)} users, {len(categories)} categories, "
            f"{len(books)} books, ~{len(books) * comments_per_book} comments, "
            f"{n_borrow_records} borrow records."
        ))

    # ---- individual seeders ----

    def _seed_categories(self):
        self.stdout.write("Seeding categories...")
        existing = {c.name for c in Category.objects.all()}
        to_create = [
            Category(name=name) for name in CATEGORY_NAMES if name not in existing
        ]
        Category.objects.bulk_create(to_create)
        return list(Category.objects.all())

    def _seed_users(self, n_users):
        self.stdout.write(f"Seeding {n_users} users...")
        existing_usernames = set(
            User.objects.filter(username__startswith="seeduser_").values_list(
                "username", flat=True
            )
        )
        to_create = []
        for i in range(n_users):
            username = f"seeduser_{i}"
            if username in existing_usernames:
                continue
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            user = User(
                username=username,
                first_name=first,
                last_name=last,
                email=f"{username}@example.test",
                is_admin=(i == 0),  # first seeded user is an admin, handy for testing
            )
            user.set_password("testpass123")
            to_create.append(user)
        User.objects.bulk_create(to_create)
        return list(User.objects.filter(username__startswith="seeduser_"))

    def _seed_books(self, n_books, categories):
        self.stdout.write(f"Seeding {n_books} books...")
        to_create = []
        for i in range(n_books):
            title = f"[seed] {random.choice(TITLE_WORDS_A)} {random.choice(TITLE_WORDS_B)} #{i}"
            author = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            book = Book(
                title=title,
                author=author,
                published_date=random_date(),
                description=(
                    f"A {random.choice(['gripping', 'thoughtful', 'sweeping', 'quiet', 'daring'])} "
                    f"story about {random.choice(['love', 'war', 'discovery', 'loss', 'ambition', 'family'])}."
                ),
                total_copies=random.randint(1, 10),
            )
            to_create.append(book)
        Book.objects.bulk_create(to_create, batch_size=500)

        books = list(Book.objects.filter(title__startswith="[seed]"))

        # M2M has to be set after the books exist in the DB
        self.stdout.write("Assigning categories to books...")
        through_model = Book.categories.through
        through_rows = []
        for book in books:
            for cat in random.sample(categories, k=random.randint(1, 3)):
                through_rows.append(through_model(book_id=book.id, category_id=cat.id))
        through_model.objects.bulk_create(through_rows, batch_size=1000, ignore_conflicts=True)

        return books

    def _seed_comments(self, books, users, comments_per_book):
        if not users:
            self.stdout.write(self.style.WARNING("No users to attach comments to, skipping comments."))
            return
        self.stdout.write("Seeding comments...")
        to_create = []
        for book in books:
            for _ in range(comments_per_book):
                to_create.append(
                    Comment(
                        user=random.choice(users),
                        book=book,
                        rating=random.randint(1, 5),
                        content=random.choice(COMMENT_SNIPPETS),
                    )
                )
        Comment.objects.bulk_create(to_create, batch_size=1000)

    def _seed_borrow_records(self, books, users, n_records):
        if not users:
            self.stdout.write(self.style.WARNING("No users to attach borrow records to, skipping."))
            return
        self.stdout.write(f"Seeding {n_records} borrow records...")

        # avoid violating the "one active borrowing per user/book" constraint
        # by tracking which (user, book) pairs are already active
        active_pairs = set()
        to_create = []       # BorrowedBook instances, ready for bulk_create
        planned_dates = []   # (borrow_date, return_date) pairs, same order as to_create
        attempts = 0
        max_attempts = n_records * 5

        while len(to_create) < n_records and attempts < max_attempts:
            attempts += 1
            user = random.choice(users)
            book = random.choice(books)

            is_returned = random.random() < 0.7  # 70% historical/returned, 30% active
            pair_key = (user.id, book.id)

            if not is_returned:
                if pair_key in active_pairs:
                    continue  # would violate unique-active-borrow constraint
                active_pairs.add(pair_key)

            borrow_date = random_date(2022, 2026)
            return_date = None
            if is_returned:
                # return date must be >= borrow_date (matches the CheckConstraint)
                return_date = borrow_date + timedelta(days=random.randint(1, 60))

            # IMPORTANT: the real return_date is NOT written at insert time,
            # even though we already know its planned value. Two things are
            # fighting each other here:
            #
            # 1) bulk_create() triggers auto_now_add, which forces
            #    borrow_date = today on insert. If we also inserted an old
            #    planned return_date in that same row, it would briefly be
            #    (borrow_date=today, return_date=<old date>), which fails
            #    chk_return_after_borrow immediately, before bulk_update
            #    ever runs.
            #
            # 2) The obvious fix -- insert every row with return_date=NULL,
            #    then bulk_update the real values in afterward -- has its
            #    own bug: while every row is momentarily NULL, if the SAME
            #    (user, book) pair appears twice among the planned records
            #    (e.g. one destined to end up "returned", one destined to
            #    stay "active"), both rows look active at once and collide
            #    on the one_active_borrowing_per_user_book unique index --
            #    even though their FINAL states would never actually clash.
            #
            # Fix: only rows that will genuinely stay ACTIVE get NULL at
            # insert time. Rows headed toward a "returned" final state get a
            # harmless non-null placeholder (safely >= today) instead, so
            # they never look active during the transient insert phase.
            # bulk_update then overwrites both fields with their real values
            # together, in one statement per row.
            insert_placeholder = None if return_date is None else FAR_FUTURE_PLACEHOLDER
            to_create.append(BorrowedBook(user=user, book=book, return_date=insert_placeholder))
            planned_dates.append((borrow_date, return_date))

        # Step 1: bulk_create with the placeholder/NULL scheme above.
        # borrow_date still gets auto_now_add-stamped to today, and every
        # placeholder we chose is >= today, so chk_return_after_borrow
        # always passes here, and the active-pair uniqueness is preserved.
        created = BorrowedBook.objects.bulk_create(to_create, batch_size=1000)

        # Step 2: overwrite borrow_date (and re-set return_date alongside it,
        # in the same UPDATE per row) via bulk_update. bulk_update issues raw
        # SQL and does NOT re-trigger auto_now_add, so the values stick, and
        # since both fields land in one UPDATE statement the row is never in
        # an inconsistent state that the CHECK constraint could reject.
        for obj, (borrow_date, return_date) in zip(created, planned_dates):
            obj.borrow_date = borrow_date
            obj.return_date = return_date
        BorrowedBook.objects.bulk_update(
            created, ['borrow_date', 'return_date'], batch_size=1000
        )