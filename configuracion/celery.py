from __future__ import absolute_import, unicode_literals

# Librerias Estandar
import os

# Librerías de Terceros
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuracion.settings")

app = Celery("configuracion")
app.config_from_object("django.conf:settings", namespace="CELERY")
# Tasks live in the hexagonal primary adapters, not in an installed Django app
app.autodiscover_tasks(["api.adapters.primaries.products"])
app.conf.task_events = True
