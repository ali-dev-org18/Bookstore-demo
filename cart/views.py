from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from books.models import Book
from .models import Cart, CartItem


def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = _get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, 'Added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))


def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.info(request, 'Removed from cart.')
    return redirect('cart:cart_detail')


def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart:cart_detail')
