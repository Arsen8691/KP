from django.urls import path
from .views import catalog_view
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
]