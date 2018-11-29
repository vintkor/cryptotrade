from cryptotrade.celery import app
from awards.utils import start_point_awadr


@app.task
def start_point_awadr_task():
    start_point_awadr()
