from cryptotrade.celery import app
from finance.payments_utils.block_io import start_block_io_checker
from finance.utils import blockio_transfer_usd_to_user_balance


@app.task(name='finance.start_block_io_checker_task')
def start_block_io_checker_task():
    start_block_io_checker()


@app.task(name='finance.blockio_transfer_usd_to_user_balance_task')
def blockio_transfer_usd_to_user_balance_task():
    blockio_transfer_usd_to_user_balance()
