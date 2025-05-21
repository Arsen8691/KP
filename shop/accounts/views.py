from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from order.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Ищем пользователя по email
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Неверный email или пароль')
    
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=email).exists():  # Используем email как username
            messages.error(request, 'Пользователь с таким email уже существует')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            return redirect('/')  
    
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    orders_with_totals = []
    total_spent = 0
    for order in orders:
        total = sum(item.product.price * item.quantity for item in order.items.all())
        orders_with_totals.append((order, total))
        total_spent += total

    return render(request, 'accounts/profile.html', {
        'user': user,
        'orders_with_totals': orders_with_totals,
        'total_spent': total_spent,
        'orders_count': orders.count(),
    })