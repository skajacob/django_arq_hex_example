"""In-memory fakes of the secondary ports, used to unit test the engine"""
import itertools
import typing
from datetime import date

from api.engine.domain.entities import entities_alarms, entities_products
from api.engine.use_cases.ports.secondaries import repository_alarms
from api.engine.use_cases.ports.secondaries import repository_products


class FakeAlarmRepository(repository_alarms.AlarmRepository):
    def __init__(self):
        self.alarms: typing.List[entities_alarms.Alarm] = []
        self._ids = itertools.count(1)

    def list_alarms(self):
        return list(self.alarms)

    def get_alarm_by_date(self, from_date, to_date):
        return [a for a in self.alarms if from_date <= str(a.alert_date) <= to_date]

    def get_alarm_by_product_id_type(self, product_id, alert_type):
        return [
            a
            for a in self.alarms
            if a.product_id == product_id and a.alert_type == alert_type
        ]

    def create_alarm(self, product_id, alert_type, alert_date, is_active):
        alarm = entities_alarms.Alarm(
            id=next(self._ids),
            product_id=product_id,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=is_active,
        )
        self.alarms.append(alarm)
        return [alarm]

    def update_alarm(self, id, product_id, alert_type, alert_date, is_active):
        alarm = next(a for a in self.alarms if a.id == id)
        if alert_type is not None:
            alarm.alert_type = alert_type
        if alert_date is not None:
            alarm.alert_date = alert_date
        if is_active is not None:
            alarm.is_active = is_active
        return [alarm]


class FakeProductRepository(repository_products.ProductRepository):
    def __init__(self):
        self.products: typing.Dict[int, entities_products.Product] = {}
        self._ids = itertools.count(1)

    def list_products(self):
        return list(self.products.values())

    def get_product_without_asigned_alarms(self):
        return [p for p in self.products.values() if not p.alarms]

    def get_product_with_alarms(self, from_date, to_date):
        return [
            p
            for p in self.products.values()
            if from_date <= str(p.expiry_date) <= to_date
        ]

    def get_product(self, id_product):
        return self.products[id_product]

    def create_product(self, product_name, description, stock, expiry_date):
        product = entities_products.Product(
            id=next(self._ids),
            product_name=product_name,
            description=description,
            stock=stock,
            expiry_date=expiry_date,
            alarms=[],
        )
        self.products[product.id] = product
        return product

    def update_product(self, id, product_name, description, stock, expiry_date):
        product = self.products[id]
        if stock is not None:
            product.stock = stock
        if product_name is not None:
            product.product_name = product_name
        return product

    def delete_product(self, id):
        del self.products[id]


def make_product(product_id=1, expiry_date: date = date(2030, 1, 20), alarms=None):
    return entities_products.Product(
        id=product_id,
        product_name=f"product-{product_id}",
        description="desc",
        stock=5,
        expiry_date=expiry_date,
        alarms=alarms or [],
    )
