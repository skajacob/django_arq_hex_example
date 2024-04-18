from apps.backoffice.models.administrators import Administrator

# Librerías de Terceros
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

PRODUCT_ID = 1


class ProductsAPITest(TestCase):
    """API for testing Product's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def get_credentials(self, email, password):
        url = reverse("token_obtain")
        response = self.client.post(url, {"email": email, "password": password})
        return response.data

    def setUp(self) -> None:
        self.client = APIClient()

        self.email = "dj-superadmin@paycode.io"
        self.password = "admin123"
        self.user = Administrator.objects.get(email=self.email)
        self.api_authentication(self.user.email, self.password)

    def api_authentication(self, email: str, password: str):
        credentials = self.get_credentials(email, password)
        token = credentials.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_products(self):
        url = reverse("crud-products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_products(self):
        url = reverse("crud-products")
        payload = {"name": "string", "paternal_surname": "string", "email": "string9"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        response = self.client.get(url_query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        payload = {"name": "string", "paternal_surname": "string", "email": "string9"}
        response = self.client.put(url_query_params, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_products(self):
        url_query_params = "%s?product_id=%s" % (reverse("crud-products"), PRODUCT_ID)
        response = self.client.delete(url_query_params)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
