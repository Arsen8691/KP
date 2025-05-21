from django.contrib import admin
from catalog.models import Product, Category, Review
from order.models import DeliveryAddress
from order.models import Order

admin.site.register(Review)
admin.site.register(DeliveryAddress)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)