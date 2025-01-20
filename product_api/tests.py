import pytest
from rest_framework import status
from django.urls import reverse
from product.models import Product, Order
from rest_framework.test import APIClient


@pytest.fixture
def create_products():
    """Fixture to create products for testing."""
    product1 = Product.objects.create(name="Product 1", price=100)
    product2 = Product.objects.create(name="Product 2", price=200)
    return [product1, product2]


@pytest.fixture
def api_client():
    """Fixture to set up the APIClient."""
    return APIClient()


@pytest.mark.django_db
def test_create_order_valid_data(api_client, create_products):
    """Test creating an order with valid data."""
    url = reverse('order-create')
    product_ids = [product.id for product in create_products]
    data = {
        'product': product_ids,
        'table_number': 'A1'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    order = Order.objects.last()
    assert order.table_number == 'A1'
    assert order.total_amount == sum([product.price for product in create_products])
    assert order.status == 'MODERATION'
    assert set(order.product.values_list('id', flat=True)) == set(product_ids)


@pytest.mark.django_db
def test_create_order_no_products(api_client):
    """Test that validation error is raised if no products are selected."""
    url = reverse('order-create')
    data = {
        'product': [],
        'table_number': 'A1'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'product' in response.data
    assert response.data['product'] == ['At least one product must be selected.']


@pytest.mark.django_db
def test_create_order_empty_table_number(api_client, create_products):
    """Test that validation error is raised if table_number is empty."""
    url = reverse('order-create')
    product_ids = [product.id for product in create_products]
    data = {
        'product': product_ids,
        'table_number': ''
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'table_number' in response.data
    assert response.data['table_number'] == ['Table number cannot be empty.']


@pytest.mark.django_db
def test_create_order_invalid_product(api_client):
    """Test that validation error is raised if one of the products does not exist."""
    url = reverse('order-create')
    data = {
        'product': [99999],
        'table_number': 'A1'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'product' in response.data
    assert response.data['product'] == ['One or more selected products do not exist.']
