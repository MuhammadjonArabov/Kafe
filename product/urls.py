from django.urls import path
from .views import order_products, index

urlpatterns = [
    path('order/', order_products, name='order_products'),
    path('', index, name='index'),
]
