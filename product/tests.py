import pytest
from django.urls import reverse
from django.test import Client
from .models import Category, Product, Order

@pytest.mark.django_db
class TestOrderViews:

    def setup_method(self):
        """Setup test data"""
        self.client = Client()
        self.category = Category.objects.create(name="Drinks")
        self.product1 = Product.objects.create(name="Coffee", price=5.0, category=self.category)
        self.product2 = Product.objects.create(name="Tea", price=3.0, category=self.category)
        self.order = Order.objects.create(table_number="5", status="MODERATION", total_amount=0)

    def test_order_products_get(self):
        """Test if the order products page loads correctly"""
        response = self.client.get(reverse('order_products'))
        assert response.status_code == 200
        assert b"Ordering a product" in response.content

    def test_order_products_post_valid(self):
        """Test creating an order with valid data"""
        response = self.client.post(reverse('order_products'), {
            'table_number': '10',
            'product_id': [self.product1.id, self.product2.id]
        })

        assert response.status_code == 302
        assert Order.objects.count() == 2
        new_order = Order.objects.latest('id')
        assert new_order.total_amount == 8.0

    def test_order_products_post_no_products(self):
        """Test order creation with no products selected"""
        response = self.client.post(reverse('order_products'), {'table_number': '10'})
        assert response.status_code == 200
        assert b"At least one product must be selected." in response.content

    def test_orders_list_view(self):
        """Test if the orders list page loads correctly"""
        response = self.client.get(reverse('orders_list'))
        assert response.status_code == 200
        assert self.order in response.context['orders']

    def test_update_order_status(self):
        """Test updating an order's status"""
        response = self.client.post(reverse('update_order_status', args=[self.order.id]), {'status': 'APPROVED'})
        assert response.status_code == 302
        self.order.refresh_from_db()
        assert self.order.status == 'APPROVED'

    def test_delete_order(self):
        """Test deleting an order"""
        order_count_before = Order.objects.count()
        response = self.client.post(reverse('delete_order', args=[self.order.id]))
        assert response.status_code == 302
        assert Order.objects.count() == order_count_before - 1

    def test_total_amount_view(self):
        """Test total amount statistics page"""
        self.order.status = 'SOLD'
        self.order.total_amount = 15.0
        self.order.save()

        response = self.client.get(reverse('total_amount'))
        assert response.status_code == 200
        assert b"Total Revenue" in response.content
