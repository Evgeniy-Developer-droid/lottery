from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lotery.settings')
app = Celery("Lotery")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-5-minute': {
        'task': 'public.tasks.canceled_lottery',
        'schedule': 10,
    },
}
app.conf.timezone = 'UTC'
