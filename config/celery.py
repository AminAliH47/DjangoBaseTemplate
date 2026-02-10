from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps

from config import envs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(envs.PROJECT_TITLE)
app.conf.enable_utc = False

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
