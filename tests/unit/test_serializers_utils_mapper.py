"""Unit tests for serializer validation, view helpers and the ORM mapper"""
from datetime import date, timedelta
from types import SimpleNamespace

from django.test import SimpleTestCase

from api.adapters.primaries.products import products_serializer, utils
from api.adapters.secondaries.db_orm import orm_mapper
from api.engine.domain.entities import entities_alarms
from api.engine.domain.exceptions import exceptions_dates
from tests.unit import fakes


class ValidateFieldsTests(SimpleTestCase):
    def test_expiry_date_in_the_past_is_invalid(self):
        with self.assertRaises(exceptions_dates.InvalidDate):
            products_serializer.validate_fields(
                {"expiry_date": date.today() - timedelta(days=1)}
            )

    def test_inverted_search_dates_are_invalid(self):
        with self.assertRaises(exceptions_dates.InvalidSearchDate):
            products_serializer.validate_fields(
                {"from_date": date(2030, 2, 1), "to_date": date(2030, 1, 1)}
            )

    def test_valid_dates_pass(self):
        products_serializer.validate_fields(
            {
                "expiry_date": date.today() + timedelta(days=1),
                "from_date": date(2030, 1, 1),
                "to_date": date(2030, 2, 1),
            }
        )


class ProductGeneratorDataTests(SimpleTestCase):
    @staticmethod
    def _alarm(days_from_today, is_active):
        return entities_alarms.Alarm(
            id=1,
            product_id=1,
            alert_type="x",
            alert_date=date.today() + timedelta(days=days_from_today),
            is_active=is_active,
        )

    def test_alarm_detail_for_future_alarm(self):
        product = fakes.make_product(1, alarms=[self._alarm(4, True)])
        detail = utils.product_generator_data([product])[0]["alarms"][0]["detail"]

        self.assertFalse(detail["is_expired"])
        self.assertEqual(detail["days_until_activation"], 4)

    def test_alarm_detail_for_expired_alarm(self):
        product = fakes.make_product(1, alarms=[self._alarm(-2, False)])
        detail = utils.product_generator_data([product])[0]["alarms"][0]["detail"]

        self.assertTrue(detail["is_expired"])
        self.assertEqual(detail["days_expired"], 2)


class OrmMapperTests(SimpleTestCase):
    def test_product_orm_is_mapped_to_entity_with_alarms(self):
        alarm_orm = SimpleNamespace(
            id=7,
            product_id=1,
            alert_type="t",
            alert_date=date(2030, 1, 1),
            is_active=True,
        )
        product_orm = SimpleNamespace(
            id=1,
            product_name="milk",
            description="d",
            stock=3,
            expiry_date=date(2030, 1, 10),
            alarms=SimpleNamespace(all=lambda: [alarm_orm]),
        )

        product = orm_mapper.constructor_products_entities(product_orm)

        self.assertEqual(product.product_name, "milk")
        self.assertEqual(product.alarms[0].id, 7)
        self.assertEqual(product.alarms[0].alert_type, "t")
