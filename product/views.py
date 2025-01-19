from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, Category, Order, OrderItem

from django.shortcuts import render, redirect
from django.db import transaction
from .models import Category, Product, Order, OrderItem


def order_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    if request.method == "POST":
        table_number = request.POST.get("table_number")
        selected_products = []

        for product_id in request.POST:
            if product_id.startswith("quantity_"):
                try:
                    pid = int(product_id.split('_')[1])
                    qty = int(request.POST[product_id])
                    if qty > 0:
                        selected_products.append((pid, qty))
                except (ValueError, IndexError):
                    continue

        if selected_products:
            try:
                with transaction.atomic():
                    total_amount = sum(Product.objects.get(id=pid).price * qty for pid, qty in selected_products)

                    order = Order.objects.create(
                        table_number=table_number,
                        status='MODERATION'
                    )

                    for product_id, quantity in selected_products:
                        OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity)

                return redirect("order_success")

            except Product.DoesNotExist:
                return redirect("order_products")

    return render(request, "order.html", {"categories": categories, "products": products})


def index(request):
    return render(request, "base.html")