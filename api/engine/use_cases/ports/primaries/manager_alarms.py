"""Primary ports for alarms service"""
# Standard Libraries
# Librerias Estandar
import typing
import abc
from datetime import date

# Entity
from api.engine.domain.entities import entities_alarms as entity
from api.engine.domain.entities import entities_products as entity_products


class AlarmManager(abc.ABC):
    """class to define the manager for alarm engine"""

    @abc.abstractmethod
    def list_alarms(
        self,
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def get_alarm_by_date(
        self, from_date: str, to_date: str
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def get_alarm_by_product_id_type(
        self, product_id: int, alert_type: str
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def create_alarm(
        self,
        product_id: int,
        alert_type: str,
        alert_date: date,
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def update_alarm(
        self,
        id: int,
        product_id: typing.Optional[int],
        alert_type: typing.Optional[str],
        alert_date: typing.Optional[date],
        is_active: typing.Optional[bool],
    ) -> typing.List[entity.Alarm]:
        ...

    @abc.abstractmethod
    def create_expiry_alarms(
        self, products: typing.List[entity_products.Product]
    ) -> None:
        ...

    @abc.abstractmethod
    def refresh_alarms_status(self) -> int:
        ...
