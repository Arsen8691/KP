from .models import CartItem
from django.db.models import Sum

def cart_item_count(request):
    if request.user.is_authenticated:
        result = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))
        count = result['total'] or 0
    else:
        count = 0
    return {'cart_item_count': count}