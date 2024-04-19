from api.adapters.secondaries.db_orm.repository_implementation_alarms import (
    Alarm as AlarmORM,
)
from api.engine.use_cases.ports.secondaries import repository_alarms as repository

# orm
from apps.webApp.models import products as alarm_models


def constructor_alarms(
    alarms_orm_model: alarm_models.Alarm,
) -> repository.AlarmRepository:
    return AlarmORM(alarms_orm_model=alarms_orm_model)
