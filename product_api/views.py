from product.models import Order, Product, Category
from rest_framework import generics
from .serializers import OderCreateSerializers

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OderCreateSerializers
