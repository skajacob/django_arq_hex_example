"""Integration tests: Celery tasks (worker logic) against the database"""
import contextlib
from datetime import date, timedelta

from django.core import mail
from django.test import TestCase

from api.adapters.primaries.products import tasks
from apps.webApp.models import products as models
from config.celery import app


@contextlib.contextmanager
def override_eager():
    """Run .delay() in-process so no broker is needed"""
    app.conf.task_always_eager = True
    try:
        yield
    finally:
        app.conf.task_always_eager = False


def _product(name="milk", days_to_expire=30):
    return models.Product.objects.create(
        product_name=name,
        description="d",
        stock=1,
        expiry_date=date.today() + timedelta(days=days_to_expire),
    )


class CreateProductAlarmsTaskTests(TestCase):
    def test_creates_10_and_5_days_before_alarms(self):
        product = _product()

        tasks.create_product_alarms()

        alarms = {a.alert_type: a for a in product.alarms.all()}
        self.assertEqual(set(alarms), {"10_days_before", "5_days_before"})
        self.assertEqual(
            alarms["10_days_before"].alert_date, product.expiry_date - timedelta(days=10)
        )
        self.assertEqual(
            alarms["5_days_before"].alert_date, product.expiry_date - timedelta(days=5)
        )
        self.assertFalse(any(a.is_active for a in alarms.values()))

    def test_is_idempotent(self):
        product = _product()
        tasks.create_product_alarms()
        tasks.create_product_alarms()
        self.assertEqual(product.alarms.count(), 2)

    def test_runs_through_celery_eager_mode(self):
        product = _product()
        with override_eager():
            tasks.create_product_alarms.delay().get()
        self.assertEqual(product.alarms.count(), 2)


class SendNotificationsTaskTests(TestCase):
    def test_sends_one_email_per_alarm_due_today(self):
        product = _product()
        models.Alarm.objects.create(
            product=product, alert_type="due", alert_date=date.today(), is_active=True
        )
        models.Alarm.objects.create(
            product=product,
            alert_type="later",
            alert_date=date.today() + timedelta(days=2),
            is_active=True,
        )

        tasks.send_notifications_for_today_alarms()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("milk", mail.outbox[0].body)

    def test_sends_nothing_without_alarms_due_today(self):
        _product()
        tasks.send_notifications_for_today_alarms()
        self.assertEqual(mail.outbox, [])
