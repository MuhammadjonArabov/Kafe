from product.models import Order, Product, Category
from rest_framework import generics
from .serializers import OrderCreateSerializers, OrderUpdateSerializers

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers

class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializers
    #http_method_names = ["PUT"]