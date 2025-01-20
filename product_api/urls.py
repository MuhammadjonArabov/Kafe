from django.urls import path
from . import views

urlpatterns = [
    path('order-create/', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('order-update/<int:pk>/', views.OrderUpdateAPIView.as_view(), name='order-update'),
    path('order-list/', views.OrderListAPIView.as_view(), name='order-list'),
    path('order-delete/<int:pk>/', views.OrderDeleteAPIView.as_view(), name='order-delete'),
    path('order-statistic/', views.OrderStatisticsView.as_view(), name='order-statistic'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
]
