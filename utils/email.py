import requests
from cryptotrade.settings import MAILGUN_ADDRESS, MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_SYSTEM_NAME, DEBUG


def send_simple_email(to_user, subject, text, html=False):
    data = dict()
    data['from'] = "{} <mailgun@{}>".format(MAILGUN_SYSTEM_NAME, MAILGUN_DOMAIN)
    data['to'] = to_user
    data['subject'] = subject
    data['text'] = text

    if html:
        data['html'] = html

    response = requests.post(
        MAILGUN_ADDRESS,
        auth=("api", MAILGUN_API_KEY),
        data=data
    )

    if DEBUG:
        print(response.json())
