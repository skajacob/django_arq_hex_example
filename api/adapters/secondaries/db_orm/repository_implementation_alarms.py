"""Alarms repository implementation"""
# Standard Libraries
# Librerias Estandar
import typing
from datetime import datetime

# Engine
from api.engine.use_cases.ports.secondaries import repository_alarms as repository
from api.engine.use_cases.factory import orm_mapper

# Entity
from api.engine.domain.entities import entities_alarms as entity

# ORM
from apps.webApp.models import products as product_models


class Alarm(repository.AlarmRepository):
    def __init__(self, alarms_orm_model: product_models.Alarm):
        self._alarms_orm_model = alarms_orm_model

    def list_alarms(self) -> typing.List[entity.Alarm]:
        return orm_mapper.constructor_alarms_entities(
            self._alarms_orm_model.objects.all()
        )

    def get_alarm_by_product_id_type(
        self, product_id: str, alert_type: str
    ) -> typing.List[entity.Alarm]:
        return orm_mapper.constructor_alarms_entities(
            self._alarms_orm_model.objects.get(
                product_id=product_id, alert_type=alert_type
            )
        )

    def get_alarm_by_date(self, from_date: str, to_date: str) -> entity.Alarm:
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        alarm = self._alarms_orm_model.objects.filter(
            alert_date__range=(from_date_obj, to_date_obj)
        ).values()
        return orm_mapper.constructor_alarms_entities(alarm)

    def create_alarm(
        self,
        product_id: int,
        alert_type: str,
        alert_date: int,
    ) -> entity.Alarm:
        is_active = True if alert_date > datetime.now().date() else False

        alarm = self._alarms_orm_model.objects.create(
            product_id=product_id,
            alert_type=alert_type,
            alert_date=alert_date,
            is_active=is_active,
        )
        alarm = [alarm]

        return orm_mapper.constructor_alarms_entities(alarm)

    def update_alarm(
        self,
        id: typing.Optional[int],
        product_id: typing.Optional[str],
        alert_type: typing.Optional[str],
        alert_date: typing.Optional[int],
        is_active: typing.Optional[str],
    ) -> entity.Alarm:
        alarm = self._alarms_orm_model.objects.get(product_id=product_id)
        alarm.alert_type = alert_type if alert_type else alarm.alert_type
        alarm.alert_date = alert_date if alert_date else alarm.alert_date
        alarm.is_active = is_active if is_active else alarm.is_active
        alarm.save(
            update_fields=[
                "alert_type",
                "alert_date",
                "is_active",
            ]
        )

        return orm_mapper.constructor_alarms_entities(alarm)
