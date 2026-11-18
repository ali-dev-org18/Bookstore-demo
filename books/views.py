from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, Category


def home(request):
    featured = Book.objects.filter(is_featured=True)[:8]
    new_books = Book.objects.filter(is_new=True)[:8]
    discounted = Book.objects.filter(discount_price__isnull=False)[:8]
    categories = Category.objects.all()[:6]
    return render(request, 'books/home.html', {
        'featured': featured,
        'new_books': new_books,
        'discounted': discounted,
        'categories': categories,
    })


def book_list(request):
    books = Book.objects.all()
    category_slug = request.GET.get('category')
    sort = request.GET.get('sort', '')
    q = request.GET.get('q', '')
    if category_slug:
        books = books.filter(category__slug=category_slug)
    if q:
        books = books.filter(title__icontains=q)
    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'newest':
        books = books.order_by('-created_at')
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    books_page = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'books/book_list.html', {
        'books': books_page,
        'categories': categories,
        'current_category': category_slug,
        'sort': sort,
        'q': q,
    })


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    similar = Book.objects.filter(category=book.category).exclude(id=book.id)[:4]
    return render(request, 'books/book_detail.html', {
        'book': book,
        'similar': similar,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = category.books.all()
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    books_page = paginator.get_page(page)
    return render(request, 'books/category_detail.html', {
        'category': category,
        'books': books_page,
    })
