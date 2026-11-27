"""Composition root: wires engine services with their secondary adapters"""
from api.adapters.secondaries.factory import constructor_alarms as alarms_repo
from api.adapters.secondaries.factory import constructor_products as products_repo
from api.engine.use_cases import factory as engine
from apps.webApp.models import products as products_models

products_engine = engine.constructor_manager_products(
    products_repo.constructor_products(products_models.Product)
)
alarms_engine = engine.constructor_manager_alarms(
    alarms_repo.constructor_alarms(products_models.Alarm)
)
