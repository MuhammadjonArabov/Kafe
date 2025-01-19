from django.contrib import admin
from .models import Order, Product, Category

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'get_products', 'total_amount')
    list_filter = ('status',)
    search_fields = ('table_number',)

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.product.all()])

    get_products.short_description = "Products"



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category',)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')




