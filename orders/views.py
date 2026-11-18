from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=cart.total_price,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                title=item.book.title,
                price=item.book.current_price,
                quantity=item.quantity,
            )
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully.')
        return redirect('orders:order_detail', pk=order.pk)
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
