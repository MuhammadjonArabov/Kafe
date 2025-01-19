from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, Category, Order, OrderItem

def order_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    if request.method == "POST":
        table_number = request.POST.get("table_number")
        selected_products = [
            (int(product_id.split('_')[1]), int(request.POST[product_id]))
            for product_id in request.POST if product_id.startswith("quantity_") and int(request.POST[product_id]) > 0
        ]

        if selected_products:
            with transaction.atomic():
                order = Order.objects.create(
                    table_number=table_number,
                    total_amount=sum(Product.objects.get(id=pid).price * qty for pid, qty in selected_products),
                    status='MODERATION'
                )

                for product_id, quantity in selected_products:
                    OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity)

            return redirect("order_success")

    return render(request, "order.html", {"categories": categories, "products": products})
