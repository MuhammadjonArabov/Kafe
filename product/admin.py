from django.contrib import admin
from .models import Order, Product, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_amount')
    list_filter = ('status',)
    search_fields = ('table_number',)
    actions = ['approve_orders', 'mark_as_sold']

    def approve_orders(self, request, queryset):
        queryset.update(status='APPROVED')

    def mark_as_sold(self, request, queryset):
        queryset.update(status='SOLD')

    approve_orders.short_description = "Tanlangan buyurtmalarni tasdiqlash"
    mark_as_sold.short_description = "Tanlangan buyurtmalarni sotildi deb belgilash"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'total_amount', 'image', 'category')
    list_filter = ()

