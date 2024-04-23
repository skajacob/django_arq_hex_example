from datetime import timedelta, datetime
from django_cron import CronJobBase, Schedule
from apps.webApp.models import products as products_models
from ....adapters.secondaries.factory import constructor_products as products_repo
from ....adapters.secondaries.factory import constructor_alarms as alarms_repo
from ....engine.use_cases import factory as engine
from . import utils

# Product engine implementation
products_repository = products_repo.constructor_products(products_models.Product)
products_engine = engine.constructor_manager_products(products_repository)

# Alarm engine implementation
alarms_repository = alarms_repo.constructor_alarms(products_models.Alarm)
alarms_engine = engine.constructor_manager_alarms(alarms_repository)

class CreateProductAlarmsJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Ejecutar cada 60 minutos

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cronjobs.create_product_alarms_job'

    def do(self):
        """Tarea cron para crear alarmas para productos."""
        products = products_engine.list_products()

        for product in products:
            expiry_date = product.expiry_date

            # Crear alarma 10 días antes
            existing_alarms_10_days = alarms_engine.get_alarm_by_product_id_type(
                product_id=product.id, alert_type="10_days_before"
            )
            if not existing_alarms_10_days:
                alarms_engine.create_alarm(
                    product_id=product.id,
                    alert_type="10_days_before",
                    alert_date=expiry_date - timedelta(days=10),
                    is_active=True if expiry_date > datetime.now().date() else False,
                )

            # Crear alarma 5 días antes
            existing_alarms_5_days = alarms_engine.get_alarm_by_product_id_type(
                product_id=product.id, alert_type="5_days_before"
            )
            if not existing_alarms_5_days:
                alarms_engine.create_alarm(
                    product_id=product.id,
                    alert_type="5_days_before",
                    alert_date=expiry_date - timedelta(days=5),
                    is_active=True if expiry_date > datetime.now().date() else False,
                )

class SendNotificationsForTodayAlarmsJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Ejecutar cada 60 minutos

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cronjobs.send_notifications_for_today_alarms_job'

    def do(self):
        """Tarea cron para enviar notificaciones para alarmas de hoy."""
        products = products_engine.list_products()
        today = datetime.now().date()

        for product in products:
            today_alarms = [alarm for alarm in product.alarms if alarm.alert_date == today]
            for alarm in today_alarms:
                utils.send_notification(alarm, product)