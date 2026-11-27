"""End-to-end tests against the running docker compose stack.

They exercise the real backend (HTTP), PostgreSQL, Redis and the Celery worker
container together, so they use the real database (not the Django test one) and
must be run with plain unittest inside the backend container:

    docker compose exec -e E2E_BASE_URL=http://localhost:8000 backend \
        python -m unittest tests.e2e.test_stack -v

Without E2E_BASE_URL every test is skipped.
"""
import json
import os
import time
import unittest
import urllib.error
import urllib.request
import uuid
from datetime import date, timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import redis  # noqa: E402
from django.conf import settings  # noqa: E402

from apps.backoffice.models.administrators import Administrator  # noqa: E402

BASE_URL = os.environ.get("E2E_BASE_URL", "").rstrip("/")
WORKER_TIMEOUT = int(os.environ.get("E2E_WORKER_TIMEOUT", "40"))
PASSWORD = "E2e-S3cret-pass!"


def http(method, path, body=None, token=None):
    """Return (status, json_body) for a request to the running backend"""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        f"{BASE_URL}{path}", data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        raw = error.read()
        return error.code, json.loads(raw) if raw else None


@unittest.skipUnless(BASE_URL, "E2E_BASE_URL is not set")
class StackEndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.suffix = uuid.uuid4().hex[:8]
        cls.email = f"e2e-{cls.suffix}@example.com"
        cls.user = Administrator.objects.create_superuser(
            username=f"e2e-{cls.suffix}", email=cls.email, password=PASSWORD
        )
        status, body = http(
            "POST", "/api/token/", {"email": cls.email, "password": PASSWORD}
        )
        assert status == 200, body
        cls.token = body["access"]

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_redis_is_reachable(self):
        client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        key = f"e2e:{self.suffix}"
        client.set(key, "ok", ex=30)
        self.assertEqual(client.get(key), b"ok")
        client.delete(key)

    def test_backend_serves_swagger(self):
        request = urllib.request.Request(f"{BASE_URL}/api/swagger/")
        with urllib.request.urlopen(request, timeout=15) as response:
            self.assertEqual(response.status, 200)

    def test_api_rejects_anonymous_requests(self):
        status, _ = http("GET", "/api/products")
        self.assertEqual(status, 401)

    def test_product_lifecycle_and_worker_generates_alarms(self):
        # backend + db: create the product through the API
        expiry = str(date.today() + timedelta(days=30))
        status, body = http(
            "POST",
            "/api/products",
            {
                "product_name": f"e2e-{self.suffix}",
                "description": "created by e2e",
                "stock": 3,
                "expiry_date": expiry,
            },
            self.token,
        )
        self.assertEqual(status, 201, body)
        product_id = body["data"]["id"]

        try:
            # redis + worker: enqueue the cronjob task and wait for the worker
            from api.adapters.primaries.products.tasks import create_product_alarms

            result = create_product_alarms.delay()
            result.get(timeout=WORKER_TIMEOUT)
            self.assertTrue(result.successful())

            # backend + db: the worker's alarms are visible through the API
            alarms = self._alarms_of(product_id)
            self.assertEqual(
                sorted(a["alert_type"] for a in alarms),
                ["10_days_before", "5_days_before"],
            )
            self.assertFalse(any(a["is_active"] for a in alarms))

            # update with stock=0 keeps the value (regression)
            status, body = http(
                "PUT",
                f"/api/products?product_id={product_id}",
                {
                    "product_name": f"e2e-{self.suffix}",
                    "description": "created by e2e",
                    "stock": 0,
                    "expiry_date": expiry,
                },
                self.token,
            )
            self.assertEqual(status, 200, body)
            self.assertEqual(body["data"]["stock"], 0)
        finally:
            status, _ = http(
                "DELETE", f"/api/products?product_id={product_id}", token=self.token
            )
            self.assertEqual(status, 204)

        status, _ = http(
            "DELETE", f"/api/products?product_id={product_id}", token=self.token
        )
        self.assertEqual(status, 400)

    def _alarms_of(self, product_id):
        deadline = time.time() + WORKER_TIMEOUT
        while time.time() < deadline:
            status, body = http("GET", "/api/products", token=self.token)
            self.assertEqual(status, 200, body)
            product = next(p for p in body["data"] if p["id"] == product_id)
            if product["alarms"]:
                return product["alarms"]
            time.sleep(1)
        self.fail("worker did not create the alarms in time")


if __name__ == "__main__":
    unittest.main()
