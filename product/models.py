from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    table_number = models.CharField(max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='MODERATION')
    product = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f"Table {self.table_number} - {self.status}"
