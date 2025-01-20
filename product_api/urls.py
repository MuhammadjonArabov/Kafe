from django.urls import path
from . import views

urlpatterns = [
    path('order-crud/', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('order-crud/<int:pk>/', views.OrderUpdateAPIView.as_view(), name='order-update'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
]
