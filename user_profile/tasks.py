from cryptotrade.celery import app
from utils.email import send_simple_email
from utils.mobile_phone import send_simple_sms


@app.task
def send_simple_email_task(to_user, subject, text, html=False):
    send_simple_email(to_user, subject, text, html)


@app.task
def send_simple_sms_task(phone, message):
    send_simple_sms(phone, message)
