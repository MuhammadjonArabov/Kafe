from django.urls import path
from .views import order_products, index, orders_list, update_order_status, delete_order

urlpatterns = [
    path('', index, name='index'),
    path('order/', order_products, name='order_products'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
]
