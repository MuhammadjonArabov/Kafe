from product.models import Order, Product, Category
from rest_framework import generics
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderCreateSerializers

class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderUpdateSerializers
    http_method_names = ["put"]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'price']