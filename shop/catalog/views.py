from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Review
from .forms import ReviewForm
from order.models import OrderItem 
from django.db import models
from django.db.models import Avg

def catalog_view(request):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('category')
    search_query = request.GET.get('q', '')  # получаем строку поиска

    products = Product.objects.all()

    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    if search_query:
        products = products.filter(Q(title__icontains=search_query))

    sort_option = request.GET.get('sort', '')

    if sort_option == 'rating':
        products = products.order_by('-rating')
    elif sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'catalog/catalog.html', {
    'products': products,
    'categories': categories,
    'selected_categories': selected_categories,
    'search_query': search_query,
    'sort_option': sort_option,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем пользователей, у которых есть заказ с этим товаром и статусом "assembled" или "shipped"
    buyers_ids = OrderItem.objects.filter(
        product=product,
        order__status__in=['shipped']
    ).values_list('order__user_id', flat=True).distinct()

    # Получаем отзывы от таких пользователей (максимум 5)
    reviews = Review.objects.filter(
        product=product,
        user_id__in=buyers_ids
    ).order_by('-created_at')[:5]

    # Проверяем, что текущий пользователь купил товар и заказ в нужном статусе
    user_has_purchased = False
    if request.user.is_authenticated:
        user_has_purchased = OrderItem.objects.filter(
            product=product,
            order__user=request.user,
            order__status__in=['assembled', 'shipped']
        ).exists()

    context = {
        'product': product,
        'reviews': reviews,
        'user_has_purchased': user_has_purchased,
    }
    return render(request, 'catalog/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверка, купил ли пользователь товар
    has_bought = OrderItem.objects.filter(
        product=product,
        order__user=request.user,
        order__status='shipped'  # Или нужный статус, где заказ "завершён"
    ).exists()

    if not has_bought:
        return redirect('catalog:product_detail', product_id=product.id)



    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'text': form.cleaned_data['text'],
                }
            )
            avg_rating = Review.objects.filter(product=product).aggregate(avg=models.Avg('rating'))['avg'] or 0
            product.rating = round(avg_rating)
            product.save()
            return redirect('catalog:product_detail', product_id=product.id)

    else:
        form = ReviewForm()

    return render(request, 'catalog/add_review.html', {'form': form, 'product': product})