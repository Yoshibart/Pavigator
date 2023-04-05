# path/to/your/proj/src/cfehome/celery.py
import os
from celery import Celery
from decouple import config
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pavigator.settings')

app = Celery('pavigator')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'update-database': {
        'task': 'update_database',
        'schedule': crontab(hour=23, minute=40, day_of_week=0),
        'args': (),
    },
}
app.conf.beat_schedule = {
    'update-arrivaltime': {
        'task': 'update_arrivaltime',
        'schedule': 120,
        'args': (),
    },
}

