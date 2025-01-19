from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Bu model faqat meros olish uchun


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_image/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Order(BaseModel):
    STATUS_CHOICES = [
        ('MODERATION', 'Moderation'),
        ('APPROVED', 'Approved'),
        ('SOLD', 'Sold'),
    ]

    table_number = models.CharField(max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='MODERATION')

    def total_amount(self):
        """Calculates the total cost of the order"""
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Table {self.table_number} - {self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Returns the total price of the product"""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.total_price()} )"
