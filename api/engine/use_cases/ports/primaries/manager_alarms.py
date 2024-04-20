"""Primary ports for alarms service"""
# Standard Libraries
# Librerias Estandar
import typing
import abc

# Entity
from api.engine.domain.entities import entities_alarms as entity


class AlarmManager(abc.ABC):
    """class to define the manager for alarm engine"""

    @abc.abstractmethod
    def list_alarms(
        self,
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def get_alarm(self, from_date: str, to_date: str) -> entity.Alarm:
        ...

    @abc.abstractmethod
    def create_alarm(
        self,
        product_id: str,
        alert_type: str,
        alert_date: str,
        is_active: bool,
    ) -> entity.Alarm:
        ...

    @abc.abstractmethod
    def update_alarm(
        self,
        id: int,
        product: str,
        alert_type: str,
        alert_date: str,
        is_active: bool,
    ) -> entity.Alarm:
        ...
