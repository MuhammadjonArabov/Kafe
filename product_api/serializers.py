from rest_framework import serializers
from product.models import Product, Order


class OrderCreateSerializers(serializers.ModelSerializer):
    """ Order create """
    product = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    table_number = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ['table_number', 'product']

    def to_internal_value(self, data):
        """Custom validation for table_number and product."""
        table_number = data.get('table_number', "").strip()
        product_ids = data.get('product', [])

        errors = {}

        if not table_number:
            errors['table_number'] = "Table number cannot be empty."

        if not product_ids:
            errors['product'] = "At least one product must be selected."
        else:
            existing_products = Product.objects.filter(id__in=product_ids)
            if len(existing_products) != len(product_ids):
                errors['product'] = "One or more selected products do not exist."

        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)

    def create(self, validated_data):
        """ Create status and total_amount """
        product_ids = validated_data.pop('product')
        products = Product.objects.filter(id__in=product_ids)
        total_amount = sum(product.price for product in products)

        validated_data['status'] = 'MODERATION'
        validated_data['total_amount'] = total_amount

        order = super().create(validated_data)
        order.product.set(products)

        return order


class OrderUpdateSerializers(serializers.ModelSerializer):
    """ Order status update"""
    class Meta:
        model = Order
        fields = ['status']


class ProductListSerializers(serializers.ModelSerializer):
    """ Product list """
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class OrderListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'product', 'total_amount']