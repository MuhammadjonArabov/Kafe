from django.db.models import Count, Sum
from product.models import Order, Product, Category
from rest_framework import generics
from rest_framework.response import Response
from . import serializers
from rest_framework.views import APIView
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
    filterset_fields = ['category__name']
    search_fields = ['category__name', 'name']


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.exclude(status='SOLD')
    serializer_class = serializers.OrderListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['table_number', 'status']


class OrderStatisticsView(APIView):
    def get(self, request):
        # Order status count
        status_counts = Order.objects.values('status').annotate(count=Count('id'))

        # Total amount of sold orders
        total_revenue = Order.objects.filter(status='SOLD').aggregate(total=Sum('total_amount'))['total'] or 0

        return Response({
            'order_status_counts': {item['status']: item['count'] for item in status_counts},
            'total_revenue': total_revenue
        })

class OrderDeleteAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderListSerializers
