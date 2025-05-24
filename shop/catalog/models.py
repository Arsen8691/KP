from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='foto/', blank=True, null=True)  # фото будут попадать в media/foto/
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.user.username} on {self.product.title}"
