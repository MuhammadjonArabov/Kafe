import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from product_api.models import Order
from product_api.serializers import OrderUpdateSerializers


@pytest.mark.django_db
def test_order_creation():
    order = Order.objects.create(status="MODERATION")
    assert order.status == "MODERATION"
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_order_update_serializer():
    order = Order.objects.create(status="MODERATION")
    serializer = OrderUpdateSerializers(instance=order, data={"status": "APPROVED"})
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    updated_order = Order.objects.get(id=order.id)
    assert updated_order.status == "APPROVED"


@pytest.mark.django_db
def test_order_update_api():
    client = APIClient()
    order = Order.objects.create(status="MODERATION")  # ✅ To'g'ri status

    url = reverse('order-update', kwargs={'pk': order.id})
    data = {"status": "APPROVED"}

    response = client.put(url, data, format='json')

    assert response.status_code == 200, response.data
    updated_order = Order.objects.get(id=order.id)
    assert updated_order.status == "APPROVED"


@pytest.mark.django_db
def test_order_update_api_invalid_data():
    client = APIClient()
    order = Order.objects.create(status="MODERATION")

    url = reverse('order-update', kwargs={'pk': order.id})
    data = {"status": "INVALID_STATUS"}

    response = client.put(url, data, format='json')

    assert response.status_code == 400
    assert "status" in response.data
