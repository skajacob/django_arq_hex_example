"""Service for alarms uses_cases"""
# Standard Libraries
# Librerias Estandar
import typing
from datetime import date, timedelta

# Project Libraries
from api.engine.use_cases.ports.secondaries import repository_alarms as repository
from api.engine.use_cases.ports.primaries import manager_alarms as manager

# Entity
from api.engine.domain.entities import entities_alarms as entity
from api.engine.domain.entities import entities_products as entity_products

# Business rule: alarms generated automatically before a product expires
EXPIRY_ALARM_RULES = {"10_days_before": 10, "5_days_before": 5}


class AlarmService(manager.AlarmManager):
    """class to define the service for product uses cases"""

    def __init__(self, alarms_repository: repository.AlarmRepository):
        self.alarms_repository = alarms_repository

    def list_alarms(self) -> typing.List[entity.Alarm]:
        return self.alarms_repository.list_alarms()

    def get_alarm_by_date(
        self, from_date: str, to_date: str
    ) -> typing.List[entity.Alarm]:
        return self.alarms_repository.get_alarm_by_date(
            from_date=from_date, to_date=to_date
        )

    def get_alarm_by_product_id_type(
        self, product_id: int, alert_type: str
    ) -> typing.List[entity.Alarm]:
        return self.alarms_repository.get_alarm_by_product_id_type(
            product_id=product_id, alert_type=alert_type
        )

    def create_alarm(
        self,
        product_id: int,
        alert_type: str,
        alert_date: date,
    ) -> typing.List[entity.Alarm]:
        return self.alarms_repository.create_alarm(
            product_id=product_id,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=alert_date > date.today(),
        )

    def update_alarm(
        self,
        id: int,
        product_id: typing.Optional[int],
        alert_type: typing.Optional[str],
        alert_date: typing.Optional[date],
        is_active: typing.Optional[bool],
    ) -> typing.List[entity.Alarm]:
        return self.alarms_repository.update_alarm(
            id=id,
            product_id=product_id,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=is_active,
        )

    def create_expiry_alarms(
        self, products: typing.List[entity_products.Product]
    ) -> None:
        for product in products:
            for alert_type, days in EXPIRY_ALARM_RULES.items():
                if not self.get_alarm_by_product_id_type(product.id, alert_type):
                    self.create_alarm(
                        product_id=product.id,
                        alert_type=alert_type,
                        alert_date=product.expiry_date - timedelta(days=days),
                    )
