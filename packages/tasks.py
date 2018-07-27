from cryptotrade.celery import app
from awards.utils import start_rang_award_runner


@app.task
def start_rang_award_runner_task():
    start_rang_award_runner()
