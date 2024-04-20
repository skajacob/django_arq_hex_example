"""Service for alarms uses_cases"""
# Standard Libraries
# Librerias Estandar
import typing

# Project Libraries
from api.engine.use_cases.ports.secondaries import repository_alarms as repository
from api.engine.use_cases.ports.primaries import manager_alarms as manager

# Entity
from api.engine.domain.entities import entities_alarms as entity


class AlarmService(manager.AlarmManager):
    """class to define the service for product uses cases"""

    def __init__(self, alarms_repository: repository.AlarmRepository):
        self.alarms_repository = alarms_repository

    def list_alarms(self) -> typing.List[entity.Alarm]:
        return self.alarms_repository.list_alarms()

    def get_alarm(self, from_date: str, to_date: str) -> entity.Alarm:
        return self.alarms_repository.get_alarm(from_date=from_date, to_date=to_date)

    def create_alarm(
        self,
        product_id: str,
        alert_type: str,
        alert_date: str,
        is_active: bool,
    ) -> entity.Alarm:
        alarm = self.alarms_repository.create_alarm(
            product_id=product_id,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=is_active,
        )
        return alarm

    def update_alarm(
        self,
        id: int,
        product: str,
        alert_type: str,
        alert_date: str,
        is_active: bool,
    ) -> entity.Alarm:
        alarm = self.alarms_repository.update_alarm(
            id=id,
            product=product,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=is_active,
        )
        return alarm
