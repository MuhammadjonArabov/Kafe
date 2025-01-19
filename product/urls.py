from django.urls import path
from .views import order_products

urlpatterns = [
    path('order/', order_products, name='order_products'),
]
