from django.core.management.base import BaseCommand
from books.models import Category, Book


class Command(BaseCommand):
    help = 'Seed sample categories and books'

    def handle(self, *args, **options):
        cats = ['Fiction', 'Science', 'History', 'Children', 'Technology']
        categories = {}
        for c in cats:
            cat, _ = Category.objects.get_or_create(name=c, slug=c.lower())
            categories[c] = cat
        books_data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 12.99, 9.99, True, False),
            ('1984', 'George Orwell', 'Fiction', 11.50, None, True, False),
            ('A Brief History of Time', 'Stephen Hawking', 'Science', 15.00, 12.00, False, True),
            ('Sapiens', 'Yuval Noah Harari', 'History', 18.00, None, True, False),
            ('Python Crash Course', 'Eric Matthes', 'Technology', 35.00, 29.99, True, True),
            ('Clean Code', 'Robert C. Martin', 'Technology', 40.00, None, False, False),
            ('Harry Potter', 'J.K. Rowling', 'Children', 14.00, 10.50, True, False),
            ('The Hobbit', 'J.R.R. Tolkien', 'Fiction', 13.00, None, False, True),
            ('Cosmos', 'Carl Sagan', 'Science', 16.00, 13.00, False, False),
            ('Guns Germs and Steel', 'Jared Diamond', 'History', 17.50, None, False, False),
            ('Django for Beginners', 'William Vincent', 'Technology', 30.00, 25.00, True, True),
            ('Charlotte Web', 'E.B. White', 'Children', 9.99, None, False, False),
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 12.00, 9.00, False, False),
            ('The Selfish Gene', 'Richard Dawkins', 'Science', 14.50, None, False, False),
            ('World War II', 'Antony Beevor', 'History', 20.00, 16.00, False, True),
        ]
        for title, author, cat, price, disc, featured, new in books_data:
            Book.objects.get_or_create(
                title=title,
                defaults={
                    'slug': title.lower().replace(' ', '-'),
                    'author': author,
                    'category': categories[cat],
                    'description': f'A great book: {title} by {author}.',
                    'price': price,
                    'discount_price': disc,
                    'stock': 20,
                    'is_featured': featured,
                    'is_new': new,
                }
            )
        self.stdout.write(self.style.SUCCESS('Seeded data'))