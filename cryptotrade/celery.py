import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptotrade.settings')

app = Celery('cryptotrade')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'check-award-every-each-thursday-at-16-00': {
    #     'task': 'awards.tasks.check_award3',
    #     'schedule': crontab(hour=13, minute=00, day_of_week=5)
    # },
}
