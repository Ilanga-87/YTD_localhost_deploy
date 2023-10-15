"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
import os
from celery import Celery
from celery.schedules import crontab


# this code copied from manage.py
# set the default Django settings module for the 'celery' app.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YouTubeAudio.settings')

# you change the name here
app = Celery("YouTubeAudio")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace="CELERY")

# load celery.py in django apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete_expired_audio": {
        "task": "audio.tasks.clear_expired",
        "schedule": crontab(minute=0, hour=0)  # daily at midnight
    },
    "delete_empty_blacklist": {
        "task": "audio.tasks.clear_empty",
        "schedule": crontab(minute=0, hour=0, day_of_month=2)
    },
}
