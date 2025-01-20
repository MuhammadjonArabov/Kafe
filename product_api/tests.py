import pytest
from django.urls import reverse
from rest_framework import status
from product.models import Order


@pytest.mark.django_db
def test_order_create(api_client, create_test_data):
    """Order Create test"""
    product_ids = [create_test_data["product1"].id, create_test_data["product2"].id]
    data = {
        "table_number": "T5",
        "product": product_ids
    }
    url = reverse("order-create")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 2
    assert response.data["status"] == "MODERATION"


@pytest.mark.django_db
def test_order_update(api_client, create_test_data):
    """Order status update test"""
    order = create_test_data["order"]
    url = reverse("order-update", kwargs={"pk": order.id})
    data = {"status": "APPROVED"}

    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    order.refresh_from_db()
    assert order.status == "APPROVED"


@pytest.mark.django_db
def test_order_list(api_client, create_test_data):
    """Order list test"""
    url = reverse("order-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_order_statistics(api_client, create_test_data):
    """Order statistic test"""
    create_test_data["order"].status = "SOLD"
    create_test_data["order"].save()

    url = reverse("order-statistics")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "SOLD" in response.data["order_status_counts"]
    assert response.data["total_revenue"] > 0


@pytest.mark.django_db
def test_order_delete(api_client, create_test_data):
    """Order delete test"""
    order = create_test_data["order"]
    url = reverse("order-delete", kwargs={"pk": order.id})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Order.objects.count() == 0

@pytest.mark.django_db
def test_product_list(api_client, create_test_data):
    """Product list test"""
    url = reverse("product-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_product_list_filter_by_category(api_client, create_test_data):
    """Category filter test"""
    category_name = create_test_data["category"].name
    url = reverse("product-list") + f"?category__name={category_name}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert all(product["name"] in ["Product 1", "Product 2"] for product in response.data)


@pytest.mark.django_db
def test_product_list_search(api_client, create_test_data):
    """Product search test"""
    search_term = "Product 1"
    url = reverse("product-list") + f"?search={search_term}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert any(product["name"] == search_term for product in response.data)