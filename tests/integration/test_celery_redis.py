"""Integration tests: Redis and the Celery broker/worker wiring.

They need a reachable Redis (CELERY_BROKER_URL) and are skipped otherwise, so
they run inside the docker compose stack:
    docker compose exec backend python manage.py test tests.integration
"""
import unittest
import uuid

import redis
from django.conf import settings
from django.test import SimpleTestCase
from kombu import Queue

from config.celery import app


def _redis_client():
    return redis.Redis.from_url(settings.CELERY_BROKER_URL, socket_connect_timeout=2)


def _redis_available() -> bool:
    try:
        return bool(_redis_client().ping())
    except redis.exceptions.RedisError:
        return False


class CeleryConfigTests(SimpleTestCase):
    """No redis needed: checks the Celery app wiring"""

    def test_tasks_are_registered(self):
        app.loader.import_default_modules()
        self.assertIn(
            "api.adapters.primaries.products.tasks.create_product_alarms", app.tasks
        )
        self.assertIn(
            "api.adapters.primaries.products.tasks.send_notifications_for_today_alarms",
            app.tasks,
        )

    def test_beat_schedule_points_to_registered_tasks(self):
        app.loader.import_default_modules()
        for entry in settings.CELERY_BEAT_SCHEDULE.values():
            self.assertIn(entry["task"], app.tasks)

    def test_broker_comes_from_settings(self):
        self.assertEqual(app.conf.broker_url, settings.CELERY_BROKER_URL)


@unittest.skipUnless(_redis_available(), "Redis is not reachable")
class RedisIntegrationTests(SimpleTestCase):
    def setUp(self):
        self.client = _redis_client()
        self.key = f"test:{uuid.uuid4()}"

    def tearDown(self):
        self.client.delete(self.key)

    def test_set_and_get_roundtrip(self):
        self.client.set(self.key, "value", ex=30)
        self.assertEqual(self.client.get(self.key), b"value")

    def test_celery_can_connect_to_broker(self):
        with app.connection_for_write() as connection:
            connection.ensure_connection(max_retries=1)
            self.assertTrue(connection.connected)

    def test_published_message_lands_in_the_queue(self):
        queue = f"test-queue-{uuid.uuid4()}"
        with app.connection_for_write() as connection:
            connection.Producer().publish(
                {"hello": "world"},
                routing_key=queue,
                declare=[Queue(queue, routing_key=queue)],
            )
        try:
            self.assertEqual(self.client.llen(queue), 1)
        finally:
            self.client.delete(queue)
