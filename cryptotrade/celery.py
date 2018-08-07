import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptotrade.settings')

app = Celery('cryptotrade')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'start_block_io_checker-each-5-minutes': {
        'task': 'finance.start_block_io_checker_task',
        'schedule': crontab(minute='*/1')
    },
    'blockio_transfer_usd_to_user_balance-each-5-minutes': {
        'task': 'finance.blockio_transfer_usd_to_user_balance_task',
        'schedule': crontab(minute='*/1')
    },
}
