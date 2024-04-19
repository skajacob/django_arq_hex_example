"""Constructor manager for alarms uses cases"""
# Project Libraries
from api.engine.use_cases.ports.secondaries import repository_alarms as repository
from api.engine.use_cases.ports.primaries import manager_alarms as manager
from api.engine.use_cases.services import service_alarms as service


def constructor_manager_alarms(
    alarms_repository: repository.AlarmRepository,
) -> manager.AlarmManager:
    return service.AlarmService(alarms_repository=alarms_repository)
