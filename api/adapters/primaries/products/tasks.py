from __future__ import unicode_literals, absolute_import

# Librerias Estandar
import os
from datetime import timedelta, datetime

# Librerías de Terceros
from celery.schedules import crontab

# Third party libraries
from celery import shared_task, Celery

# Proyecto
# Database imports
from .....apps.webApp.models.products import Product, Alarm

# Establece la configuración de Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuracion.settings")

# Crea una instancia de Celery
app = Celery("configuracion")

# Configuración de Celery desde Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tareas en todas las aplicaciones registradas de Django
app.autodiscover_tasks()


# Programar la tarea para que se ejecute diariamente a las 8:00 AM
app.conf.beat_schedule = {
    "create_expiry_alarms": {
        "task": "tu_app.tasks.create_expiry_alarms",
        "schedule": crontab(hour=8, minute=0),
    },
}


@shared_task
def create_expiry_alarms():
    # Obtener la fecha actual
    today = datetime.now().date()

    # Definir el rango de días para considerar como próximo a caducar
    days_threshold = 10

    # Calcular la fecha límite para considerar un producto próximo a caducar
    expiry_limit = today + timedelta(days=days_threshold)

    # Obtener los productos próximos a caducar
    expiring_products = Product.objects.filter(expiry_date__lte=expiry_limit)

    # Crear una alarma para cada producto próximo a caducar
    for product in expiring_products:
        alarm = Alarm.objects.create(
            product=product,
            alert_type="Expiry",
            alert_date=product.expiry_date,
            is_active=True,
        )
        alarm.save()
