from .models import Cart


def cart(request):
    cart_obj = None
    if request.user.is_authenticated:
        cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if session_key:
            cart_obj = Cart.objects.filter(session_key=session_key).first()
    return {'cart': cart_obj}