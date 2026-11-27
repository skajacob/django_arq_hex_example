# Models
# Librerias Estandar
from datetime import datetime

# Librerías de Terceros
from celery import shared_task

# Proyecto
from api.container import alarms_engine, products_engine

# utils
from . import utils


@shared_task
def create_product_alarms():
    """cronjob for create alarms for products"""
    try:
        products = products_engine.list_products()

        alarms_engine.create_expiry_alarms(products)
        alarms_engine.refresh_alarms_status()
    except Exception as e:
        print(f"Error al generar las alarmas automaticas del cronjob: {e}")


@shared_task
def send_notifications_for_today_alarms():
    """cronjob for send email notifications"""
    try:
        products = products_engine.list_products()
        today = datetime.now().date()
        for product in products:
            today_alarms = [
                alarm for alarm in product.alarms if alarm.alert_date == today
            ]
            for alarm in today_alarms:
                utils.send_notification(alarm, product)
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")
