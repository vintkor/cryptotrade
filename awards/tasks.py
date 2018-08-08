from cryptotrade.celery import app
from awards.utils import start_point_awadr


@app.task(name='award.start_point_awadr_task')
def start_point_awadr_task():
    start_point_awadr()
