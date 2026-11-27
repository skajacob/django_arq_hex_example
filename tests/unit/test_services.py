"""Unit tests for the engine services (no Django, no DB)"""
from datetime import date, timedelta

from django.test import SimpleTestCase

from api.engine.use_cases import factory
from tests.unit import fakes


class AlarmServiceTests(SimpleTestCase):
    def setUp(self):
        self.repository = fakes.FakeAlarmRepository()
        self.service = factory.constructor_manager_alarms(self.repository)

    def test_create_alarm_is_active_when_date_is_in_the_future(self):
        alarm = self.service.create_alarm(
            1, "custom", date.today() + timedelta(days=1)
        )[0]
        self.assertTrue(alarm.is_active)

    def test_create_alarm_is_inactive_when_date_is_today_or_past(self):
        today = self.service.create_alarm(1, "custom", date.today())[0]
        past = self.service.create_alarm(
            1, "custom", date.today() - timedelta(days=3)
        )[0]
        self.assertFalse(today.is_active)
        self.assertFalse(past.is_active)

    def test_create_expiry_alarms_creates_10_and_5_days_before(self):
        expiry = date.today() + timedelta(days=30)
        self.service.create_expiry_alarms([fakes.make_product(1, expiry)])

        by_type = {a.alert_type: a for a in self.repository.alarms}
        self.assertEqual(set(by_type), {"10_days_before", "5_days_before"})
        self.assertEqual(
            by_type["10_days_before"].alert_date, expiry - timedelta(days=10)
        )
        self.assertEqual(
            by_type["5_days_before"].alert_date, expiry - timedelta(days=5)
        )
        self.assertTrue(all(a.is_active for a in by_type.values()))

    def test_create_expiry_alarms_is_idempotent(self):
        products = [fakes.make_product(1, date.today() + timedelta(days=30))]
        self.service.create_expiry_alarms(products)
        self.service.create_expiry_alarms(products)
        self.assertEqual(len(self.repository.alarms), 2)

    def test_create_expiry_alarms_only_fills_missing_alarms(self):
        expiry = date.today() + timedelta(days=30)
        self.service.create_alarm(1, "10_days_before", expiry - timedelta(days=10))
        self.service.create_expiry_alarms([fakes.make_product(1, expiry)])
        self.assertEqual(
            sorted(a.alert_type for a in self.repository.alarms),
            ["10_days_before", "5_days_before"],
        )

    def test_create_expiry_alarms_for_expired_product_are_inactive(self):
        self.service.create_expiry_alarms(
            [fakes.make_product(1, date.today() - timedelta(days=1))]
        )
        self.assertTrue(self.repository.alarms)
        self.assertFalse(any(a.is_active for a in self.repository.alarms))

    def test_update_alarm_keeps_false_values(self):
        alarm = self.service.create_alarm(
            1, "custom", date.today() + timedelta(days=2)
        )[0]
        updated = self.service.update_alarm(alarm.id, None, None, None, False)[0]
        self.assertFalse(updated.is_active)


class ProductServiceTests(SimpleTestCase):
    def setUp(self):
        self.repository = fakes.FakeProductRepository()
        self.service = factory.constructor_manager_products(self.repository)

    def test_create_and_get_product(self):
        product = self.service.create_product("milk", "desc", 10, date(2030, 1, 1))
        self.assertEqual(self.service.get_product(product.id).product_name, "milk")

    def test_update_product_allows_zero_stock(self):
        product = self.service.create_product("milk", "desc", 10, date(2030, 1, 1))
        updated = self.service.update_product(product.id, None, None, 0, None)
        self.assertEqual(updated.stock, 0)

    def test_delete_product(self):
        product = self.service.create_product("milk", "desc", 10, date(2030, 1, 1))
        self.assertIsNone(self.service.delete_product(product.id))
        self.assertEqual(self.service.list_products(), [])

    def test_get_product_with_alarms_filters_by_range(self):
        self.service.create_product("a", "d", 1, date(2030, 1, 1))
        self.service.create_product("b", "d", 1, date(2031, 1, 1))
        found = self.service.get_product_with_alarms("2030-01-01", "2030-12-31")
        self.assertEqual([p.product_name for p in found], ["a"])
