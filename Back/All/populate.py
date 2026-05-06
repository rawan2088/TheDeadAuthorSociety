import requests

from models import Book
# from .models import Book

neededBooks = {"The Great Gatsby", "To kill a mockingbird", "1984", "Pride and Prejudice", "The Catcher in the Rye", "The Lord of the Rings", "The Hobbit", "Harry Potter and the Sorcerer's Stone", "The Chronicles of Narnia", "The Hunger Games"}
neededBooks = {"The Great Gatsby"}

#author_name
#first_publish_year
#title
#"cover_i": 10590366,

# def populate_books():
url = "https://openlibrary.org/search.json?title="    
for book in neededBooks:
    book = book.lower().replace(" ", "+")
    url += book + "&limit=1&offset=0"
    response = requests.get(url)

    print('hay')
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data['docs']:
            book_data = data['docs'][0]
            title = book_data.get('title', 'No Title')
            authors = book_data.get('author_name', ['Unknown Author'])
            published_date = book_data.get('first_publish_year', '1900-01-01')
            category = book_data.get('subject', ['Uncategorized'])[0]
            description = book_data.get('description', 'No Description')
            image_url = book_data.get('cover_i', '')

            # Create a new Book instance and save it to the database
            book = Book(
                title=title,
                author=', '.join(authors),
                published_date=published_date,
                category=category,
                description=description,
                image=image_url,
                totalCopies=10,  # Default value, you can adjust as needed
                availableCopies=10  # Default value, you can adjust as needed
            )
            book.save()
else:
    print(f'Failed to fetch data from API. Status code: {response.status_code}')
    
    # populate_books()