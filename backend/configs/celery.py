import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "fetch_privat_bank_data": {
        'task': 'core.services.currency_service.fetch_currency',
        'schedule': crontab(minute='1', hour='6')
    }
}
