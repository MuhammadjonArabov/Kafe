from django.shortcuts import render
from .models import Product, Category

def order_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'order.html', {'categories': categories, 'products': products})