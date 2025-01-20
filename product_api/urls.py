from django.urls import path
from .views import *

urlpatterns = [
    path('order/', OrderCreateAPIView.as_view(), name='order_products'),
    path('order-update/<int:pk>/', OrderUpdateAPIView.as_view(), name='order_update'),
]
