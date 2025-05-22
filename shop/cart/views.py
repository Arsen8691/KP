from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from catalog.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    next_url = request.GET.get('next', '/')
    return redirect(next_url)

@login_required
def remove_from_cart(request, product_id):
    try:
        cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart')
