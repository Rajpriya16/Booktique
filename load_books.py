import os
import pandas as pd
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from data.models import Book

# Load the CSV file
data = pd.read_csv('books.csv', on_bad_lines='skip')  # Skips bad lines

# Iterate through the rows and save each book
for index, row in data.iterrows():
    book = Book(
        bookID=row['bookID'],
        title=row['title'],
        authors=row['authors'],
        average_rating=row['average_rating'],
        isbn=row['isbn'],
        num_pages=row['num_pages'] if 'num_pages' in row else 0,
        publisher=row['publisher']
    )
    book.save()

print('Books loaded successfully.')
