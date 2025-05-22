from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from catalog.models import Product
from cart.models import CartItem
from .models import DeliveryAddress
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Order
from django.contrib import messages


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if request.method == 'POST':
        # Получаем данные формы
        full_name = request.POST.get('fullName')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        payment = request.POST.get('payment')
        address = request.POST.get('address')
        comment = request.POST.get('comment')

        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            payment_method=payment,
            comment=comment,
        )

        # Создаем позиции заказа
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Очищаем корзину пользователя
        cart_items.delete()

        return redirect('order:order_success', order_id=order.id)

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    items_count = sum(item.quantity for item in cart_items)
    email = request.user.email
    addresses = DeliveryAddress.objects.all()

    return render(request, 'order/checkout.html', {
        'total_price': total_price,
        'items_count': items_count,
        'email': email,
        'addresses': addresses,
    })



def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_success.html', {'order_number': order.id})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Проверка: если заказ не принадлежит пользователю и он не админ
    if order.user != request.user and not request.user.is_staff:
        return redirect('homepage:index')

    items = order.items.select_related('product')
    items_with_totals = [
        {
            'id': item.product.id,  
            'title': item.product.title,
            'image': item.product.image.url,
            'quantity': item.quantity,
            'price': item.product.price,
            'total': item.quantity * item.product.price
        }
        for item in items
    ]
    total_price = sum(i['total'] for i in items_with_totals)

    return render(request, 'order/order_detail.html', {
        'order': order,
        'items': items_with_totals,
        'total_price': total_price
    })