from __future__ import unicode_literals, absolute_import

# Librerias Estandar
import os

# Librerías de Terceros
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuracion.settings")

app = Celery("apps.webApp")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.task_events = True

