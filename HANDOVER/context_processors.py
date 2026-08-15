from .models import Cart

def cart_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.none()

    return {
        "cart_count": cart_items.count(),
        "mini_cart": cart_items,
    }