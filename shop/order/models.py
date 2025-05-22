from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product  # Импортируй свою модель товаров

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Обрабатывается'),
        ('assembled', 'Собран'),
        ('shipped', 'Передан'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=[('card', 'Карта'), ('cash', 'Наличные')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Неизвестно')
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"


class DeliveryAddress(models.Model):
    name = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.name
