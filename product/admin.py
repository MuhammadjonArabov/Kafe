from django.contrib import admin
from .models import Order, Product, Category

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'product', 'total_amount')
    list_filter = ('status',)
    search_fields = ('table_number',)
    actions = ['approve_orders', 'mark_as_sold']

    def approve_orders(self, request, queryset):
        queryset.update(status='APPROVED')

    def mark_as_sold(self, request, queryset):
        queryset.update(status='SOLD')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category',)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')




