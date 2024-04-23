from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

PRODUCT_ID = 1


class ProductsAPITest(BaseAPITest):
    """API for testing Product's CRUD"""

    fixtures = [
        "fixtures/data2.json",
    ]

    def test_list_products(self):
        url = reverse("crud-products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_products(self):
        url = reverse("crud-products")
        payload = {
            "product_name": "Donas Glaseadas Rellenas de Mermelada de Piña",
            "description": "Donas Glaseadas Rellenas de Mermelada de Piña Krispy Kreme",
            "stock": 200,
            "expiry_date": "2024-07-02",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        response = self.client.get(url_query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        payload = {
            "product_name": "Donas Glaseadas",
            "description": "Donas Glaseadas Krispy Kreme",
            "stock": 80,
            "expiry_date": "2024-09-10",
        }
        response = self.client.put(url_query_params, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        response = self.client.delete(url_query_params)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_alarm(self):
        url = reverse("create_alarm")
        payload = {
            "product_id": 1,
            "alert_type": "alerta custom",
            "alert_date": "2024-07-02",
            "is_active": "",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
