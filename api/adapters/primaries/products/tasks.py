# Third party libraries
# Librerias Estandar
from datetime import timedelta, datetime

# models
from apps.webApp.models import products as products_models

# Librerías de Terceros
from celery import shared_task

# Proyecto
# Product & Alarm engine imports
from ....adapters.secondaries.factory import constructor_products as products_repo
from ....adapters.secondaries.factory import constructor_alarms as alarms_repo
from ....engine.use_cases import factory as engine

# product engine implementation
products_repository = products_repo.constructor_products(products_models.Product)
products_engine = engine.constructor_manager_products(products_repository)
# Alarm engine implementation
alarms_repository = alarms_repo.constructor_alarms(products_models.Alarm)
alarms_engine = engine.constructor_manager_alarms(alarms_repository)


@shared_task
def create_product_alarms():
    product = products_engine.get_product_without_alarms()
    expiry_date = product.expiry_date

    # Crear alarma 10 días antes
    alarm = alarms_engine.create_alarm(
        product=product,
        alert_type="10_days_before",
        alert_date=expiry_date - timedelta(days=10),
        is_active=True
        if datetime.strptime(expiry_date, "%Y-%m-%d").date() > datetime.now
        else False,
    )

    # Crear alarma 5 días antes

    alarm = alarms_engine.create_alarm(
        product=product,
        alert_type="5_days_before",
        alert_date=expiry_date - timedelta(days=5),
        is_active=True
        if datetime.strptime(expiry_date, "%Y-%m-%d").date() > datetime.now
        else False,
    )
