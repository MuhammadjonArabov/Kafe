from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Order

def order_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Agar kategoriya tanlangan bo‘lsa, mahsulotlarni filtrlaymiz
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        selected_products = request.POST.getlist('product_id')  # "product_id" nomi bilan olish

        if not selected_products:  # Agar mahsulot tanlanmasa, xatolik bermaslik uchun tekshirish
            return render(request, 'order.html', {
                'categories': categories,
                'products': products,
                'error': "At least one product must be selected."
            })

        total_amount = 0

        # Buyurtmani yaratish va `total_amount=0` berish
        order = Order.objects.create(table_number=table_number, status='MODERATION', total_amount=0)

        for product_id in selected_products:
            product = Product.objects.get(id=product_id)
            total_amount += product.price  # Jami narxni hisoblash
            order.product.add(product)  # Mahsulotlarni buyurtmaga qo‘shish

        order.total_amount = total_amount  # Umumiy narxni saqlash
        order.save()

        return redirect('orders_list')  # Sahifaga qaytarish

    return render(request, 'order.html', {'categories': categories, 'products': products})


def orders_list(request):
    orders = Order.objects.exclude(status='SOLD')
    return render(request, 'orders.html', {'orders': orders})


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


def total_amount(request):
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
