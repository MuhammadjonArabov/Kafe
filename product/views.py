from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Category, Product, Order


def order_products(request):
    categories = Category.objects.all()
    category_id = request.GET.get("category")
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    if request.method == "POST":
        table_number = request.POST.get("table_number")
        selected_products = request.POST.getlist("products")

        if selected_products:
            with transaction.atomic():
                total_amount = sum(Product.objects.get(id=pid).price for pid in selected_products)
                order = Order.objects.create(
                    table_number=table_number,
                    status="MODERATION",
                    total_amount=total_amount
                )
                order.product.add(*selected_products)

            return redirect("orders_list")

    return render(request, "order.html", {"categories": categories, "products": products})


def orders_list(request):
    orders = Order.objects.prefetch_related("product").all()
    return render(request, "orders.html", {"orders": orders})


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
    return redirect("orders_list")


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
    return redirect("orders_list")


def index(request):
    return render(request, "base.html")
