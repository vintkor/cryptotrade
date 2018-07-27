import requests
from cryptotrade.settings import WEBPURSE_PASS, WEBPURSE_WPID
from cryptotrade.settings import DEBUG


def send_simple_sms(phone, message):
    url_endpoint = 'http://webpurse.net/sms/api/'
    parameters = {
        'act': 'sms',
        'wpid': WEBPURSE_WPID,
        'passapi': WEBPURSE_PASS,
        'phone': phone,
        'msg': message,
        'sender': 'CryptoTrade',
        'charset': 'utf-8',
    }
    response = requests.get(url_endpoint, params=parameters)

    if DEBUG:
        print(response)
