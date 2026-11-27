"""Integration tests: primary adapter (REST API) -> engine -> ORM -> database"""
from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from apps.backoffice.models.administrators import Administrator
from apps.webApp.models import products as models

PASSWORD = "S3cret-pass!"


def authenticated_client() -> APIClient:
    Administrator.objects.create_superuser(
        username="tester", email="tester@example.com", password=PASSWORD
    )
    client = APIClient()
    response = client.post(
        reverse("token_obtain"), {"email": "tester@example.com", "password": PASSWORD}
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


class ProductsApiTests(TestCase):
    def setUp(self):
        self.client = authenticated_client()
        self.url = reverse("crud-products")
        self.expiry = str(date.today() + timedelta(days=30))
        self.payload = {
            "product_name": "milk",
            "description": "whole milk",
            "stock": 10,
            "expiry_date": self.expiry,
        }

    def _create(self, **overrides):
        return self.client.post(self.url, {**self.payload, **overrides})

    def test_requires_authentication(self):
        response = APIClient().get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_and_list_product(self):
        created = self._create()
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created.data["data"]["product_name"], "milk")

        listed = self.client.get(self.url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data["data"]), 1)

    def test_create_product_creates_10_and_5_days_alarms_immediately(self):
        created = self._create()

        alarms = created.data["data"]["alarms"]
        self.assertEqual(
            sorted(a["alert_type"] for a in alarms),
            ["10_days_before", "5_days_before"],
        )
        detail = {a["alert_type"]: a["detail"] for a in alarms}
        self.assertEqual(detail["10_days_before"]["days_until_activation"], 20)
        self.assertEqual(detail["5_days_before"]["days_until_activation"], 25)
        self.assertFalse(detail["5_days_before"]["is_expired"])

    def test_list_includes_alarm_detail(self):
        self._create()
        alarm = self.client.get(self.url).data["data"][0]["alarms"][0]
        self.assertEqual(
            set(alarm["detail"]),
            {"is_active", "is_expired", "days_until_activation", "days_expired"},
        )

    def test_filter_by_alert_status(self):
        self._create()
        past = str(date.today() + timedelta(days=6))
        self._create(product_name="yogurt", expiry_date=past)
        self._create(
            product_name="cheese", expiry_date=str(date.today() + timedelta(days=3))
        )

        unfiltered = self.client.get(self.url)
        self.assertEqual(len(unfiltered.data["data"]), 3)

        pending = self.client.get(self.url, {"is_active": "false"})
        names = sorted(p["product_name"] for p in pending.data["data"])
        self.assertEqual(names, ["milk", "yogurt"])

        active = self.client.get(self.url, {"is_active": "true"})
        self.assertEqual(
            sorted(p["product_name"] for p in active.data["data"]),
            ["cheese", "yogurt"],
        )
        self.assertTrue(
            all(a["detail"]["is_active"] for p in active.data["data"] for a in p["alarms"])
        )

        expired = self.client.get(self.url, {"is_expired": "true"})
        self.assertEqual(
            sorted(p["product_name"] for p in expired.data["data"]),
            ["cheese", "yogurt"],
        )

    def test_create_duplicate_product_returns_400(self):
        self._create()
        response = self._create()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_invalid_payload_returns_400(self):
        response = self.client.post(self.url, {"product_name": "only-name"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_with_zero_stock(self):
        product_id = self._create().data["data"]["id"]

        response = self.client.put(
            f"{self.url}?product_id={product_id}", {**self.payload, "stock": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(id=product_id).stock, 0)

    def test_update_missing_product_returns_400(self):
        response = self.client.put(f"{self.url}?product_id=9999", self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        product_id = self._create().data["data"]["id"]

        response = self.client.delete(f"{self.url}?product_id={product_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Product.objects.filter(id=product_id).exists())

    def test_delete_missing_product_returns_400(self):
        response = self.client.delete(f"{self.url}?product_id=9999")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_by_expiry_date_range(self):
        self._create(product_name="inside", expiry_date="2030-06-01")
        self._create(product_name="outside", expiry_date="2032-06-01")

        response = self.client.get(
            self.url, {"from_date": "2030-01-01", "to_date": "2030-12-31"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [p["product_name"] for p in response.data["data"]], ["inside"]
        )

    def test_list_by_empty_expiry_date_range_returns_404(self):
        response = self.client.get(
            self.url, {"from_date": "1990-01-01", "to_date": "1990-12-31"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AlarmsApiTests(TestCase):
    def setUp(self):
        self.client = authenticated_client()
        self.url = reverse("create_alarm")
        self.product = models.Product.objects.create(
            product_name="milk",
            description="d",
            stock=1,
            expiry_date=date.today() + timedelta(days=30),
        )

    def test_create_alarm_is_visible_in_product_listing(self):
        alert_date = str(date.today() + timedelta(days=3))

        response = self.client.post(
            self.url,
            {"product_id": self.product.id, "alert_type": "custom", "alert_date": alert_date},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["data"]["is_active"])

        listed = self.client.get(reverse("crud-products"))
        alarms = listed.data["data"][0]["alarms"]
        self.assertEqual([a["alert_type"] for a in alarms], ["custom"])

    def test_create_alarm_for_missing_product_returns_400(self):
        response = self.client.post(
            self.url,
            {"product_id": 9999, "alert_type": "custom", "alert_date": "2030-01-01"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Alarm.objects.count(), 0)
