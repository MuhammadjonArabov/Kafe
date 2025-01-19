from django.urls import path
from .views import order_products, total_amount, orders_list, update_order_status, delete_order

urlpatterns = [
    path('', order_products, name='order_products'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('total_amount/', total_amount, name='total_amount'),
]
