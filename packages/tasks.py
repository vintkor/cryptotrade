from cryptotrade.celery import app
from awards.utils import start_rang_award_runner, start_multi_level_bonus_runner


@app.task
def start_rang_award_runner_task():
    start_rang_award_runner()


@app.task
def start_multi_level_bonus_runner_task(user_id, amount, package_history_id):
    start_multi_level_bonus_runner(user_id, amount, package_history_id)
