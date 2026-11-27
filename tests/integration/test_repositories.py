"""Integration tests: secondary adapters (ORM repositories) against the database"""
from datetime import date, timedelta

from django.test import TestCase

from api.adapters.secondaries.factory import constructor_alarms, constructor_products
from api.engine.domain.exceptions import exceptions_products
from apps.webApp.models import products as models


class ProductRepositoryTests(TestCase):
    def setUp(self):
        self.repository = constructor_products.constructor_products(models.Product)
        self.expiry = date.today() + timedelta(days=30)

    def _create(self, name="milk", stock=10, expiry=None):
        return self.repository.create_product(name, "desc", stock, expiry or self.expiry)

    def test_create_and_get_product(self):
        created = self._create()
        fetched = self.repository.get_product(created.id)

        self.assertEqual(fetched.product_name, "milk")
        self.assertEqual(fetched.alarms, [])

    def test_create_duplicate_name_raises_domain_exception(self):
        self._create()
        with self.assertRaises(exceptions_products.ProductAlreadyExist):
            self._create()

    def test_get_missing_product_raises_domain_exception(self):
        with self.assertRaises(exceptions_products.ProductDoesNotExist):
            self.repository.get_product(9999)

    def test_update_product_allows_zero_stock(self):
        created = self._create(stock=10)
        updated = self.repository.update_product(created.id, None, None, 0, None)

        self.assertEqual(updated.stock, 0)
        self.assertEqual(updated.product_name, "milk")

    def test_update_missing_product_raises_domain_exception(self):
        with self.assertRaises(exceptions_products.ProductDoesNotExist):
            self.repository.update_product(9999, "x", None, None, None)

    def test_delete_product(self):
        created = self._create()
        self.repository.delete_product(created.id)
        self.assertEqual(self.repository.list_products(), [])

    def test_delete_missing_product_raises_domain_exception(self):
        with self.assertRaises(exceptions_products.ProductDoesNotExist):
            self.repository.delete_product(9999)

    def test_get_product_with_alarms_filters_by_expiry_range(self):
        inside = self._create("inside", expiry=date(2030, 6, 1))
        self._create("outside", expiry=date(2032, 6, 1))

        found = self.repository.get_product_with_alarms("2030-01-01", "2030-12-31")

        self.assertEqual([p.id for p in found], [inside.id])

    def test_get_product_without_alarms(self):
        with_alarm = self._create("with-alarm")
        without_alarm = self._create("without-alarm")
        models.Alarm.objects.create(
            product_id=with_alarm.id,
            alert_type="x",
            alert_date=self.expiry,
            is_active=True,
        )

        found = self.repository.get_product_without_asigned_alarms()

        self.assertEqual([p.id for p in found], [without_alarm.id])

    def test_list_products_includes_alarms(self):
        created = self._create()
        models.Alarm.objects.create(
            product_id=created.id, alert_type="x", alert_date=self.expiry, is_active=True
        )
        products = self.repository.list_products()
        self.assertEqual(len(products[0].alarms), 1)


class AlarmRepositoryTests(TestCase):
    def setUp(self):
        self.repository = constructor_alarms.constructor_alarms(models.Alarm)
        self.product = models.Product.objects.create(
            product_name="milk",
            description="d",
            stock=1,
            expiry_date=date.today() + timedelta(days=30),
        )
        self.alert_date = date.today() + timedelta(days=5)

    def _create(self, alert_type="custom", is_active=True):
        return self.repository.create_alarm(
            self.product.id, alert_type, self.alert_date, is_active
        )[0]

    def test_create_alarm(self):
        alarm = self._create()
        self.assertEqual(alarm.product_id, self.product.id)
        self.assertTrue(alarm.is_active)

    def test_get_alarm_by_product_id_type_returns_list(self):
        self._create("a")
        self._create("b")

        found = self.repository.get_alarm_by_product_id_type(self.product.id, "a")

        self.assertEqual([a.alert_type for a in found], ["a"])
        self.assertEqual(
            self.repository.get_alarm_by_product_id_type(self.product.id, "zzz"), []
        )

    def test_get_alarm_by_date_range(self):
        self._create()
        in_range = self.repository.get_alarm_by_date(
            str(self.alert_date), str(self.alert_date)
        )
        out_of_range = self.repository.get_alarm_by_date("2000-01-01", "2000-01-02")

        self.assertEqual(len(in_range), 1)
        self.assertEqual(out_of_range, [])

    def test_update_alarm_by_id_keeps_false_is_active(self):
        alarm = self._create(is_active=True)

        updated = self.repository.update_alarm(alarm.id, None, "renamed", None, False)[0]

        self.assertEqual(updated.alert_type, "renamed")
        self.assertFalse(updated.is_active)
        self.assertFalse(models.Alarm.objects.get(id=alarm.id).is_active)

    def test_list_alarms(self):
        self._create("a")
        self._create("b")
        self.assertEqual(len(self.repository.list_alarms()), 2)
