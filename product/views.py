from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Order

def order_products(request):
    """
    Handles ordering products. Displays available products and categories.
    Processes order submissions and saves selected products with total amount.
    """
    categories = Category.objects.all()
    products = Product.objects.all()

    # Filter products by category if selected
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        selected_products = request.POST.getlist('product_id')

        # Ensure at least one product is selected
        if not selected_products:
            return render(request, 'order.html', {
                'categories': categories,
                'products': products,
                'error': "At least one product must be selected."
            })

        total_amount = 0

        # Create a new order with default total_amount=0
        order = Order.objects.create(table_number=table_number, status='MODERATION', total_amount=0)

        # Calculate total amount and add selected products to the order
        for product_id in selected_products:
            product = Product.objects.get(id=product_id)
            total_amount += product.price
            order.product.add(product)

        # Update and save the total amount
        order.total_amount = total_amount
        order.save()

        return redirect('orders_list')

    return render(request, 'order.html', {'categories': categories, 'products': products})


def orders_list(request):
    """
    Displays a list of all orders that are not marked as SOLD.
    """
    orders = Order.objects.exclude(status='SOLD')
    return render(request, 'orders.html', {'orders': orders})


def update_order_status(request, order_id):
    """
    Updates the status of a specific order.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
    return redirect("orders_list")


def delete_order(request, order_id):
    """
    Deletes a specific order.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
    return redirect("orders_list")


def total_amount(request):
    """
    Calculates and displays order statistics:
    - Number of orders in MODERATION
    - Number of APPROVED orders
    - Number of SOLD orders
    - Total revenue from SOLD orders
    """
    moderation_count = Order.objects.filter(status='MODERATION').count()
    approved_count = Order.objects.filter(status='APPROVED').count()
    sold_orders = Order.objects.filter(status='SOLD')

    sold_count = sold_orders.count()
    total_revenue = sum(order.total_amount for order in sold_orders)

    context = {
        "moderation_count": moderation_count,
        "approved_count": approved_count,
        "sold_count": sold_count,
        "total_revenue": total_revenue,
    }

    return render(request, "total_amount.html", context)
