"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
import os
from celery import Celery
from celery.schedules import crontab


# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
# from YouTubeAudio import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YouTubeAudio.settings')

# you change the name here
app = Celery("YouTubeAudio", broker="redis://127.0.0.1:6379")
# app.config_from_object(celeryconfig)

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace="CELERY")

# load celery.py in django apps
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "delete_expired_audio": {
        "task": "audio.tasks.clear_expired",
        "schedule": crontab(minute=0, hour='*')
    }
}