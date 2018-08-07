from cryptotrade.settings import (
    BITCOIN_CODE, 
    BLOCKIO_BITCOIN_API_KEY,
    BLOCKIO_LITECOIN_API_KEY,
    BLOCKIO_DOGECOIN_API_KEY,
    BLOCKIO_SECRET_PIN,
)
from block_io import BlockIo
from finance.models import BlockIOWallet
import decimal
import requests


class BlockIOChecker:
    
    def __init__(self, api_key, secret_pin):
        self._api_key = api_key
        self._secret_pin = secret_pin
        self._version = 2
        self._block_io = BlockIo(self._api_key, self._secret_pin, self._version)
        self._set_wallets()

    def _set_wallets(self):
        self._wallets = BlockIOWallet.objects.filter(balance=0)

    def _get_addresses(self):
        return ','.join([i.wallet for i in self._wallets])

    def get_wallets_data(self):
        response = self._block_io.get_address_balance(addresses=self._get_addresses())
        wallets_data_list = list()

        if response['status'] == 'success':
            balances = response['data']['balances']

            for balance in balances:
                wallet_info = balance['label'].split('_')
                wallets_data_list.append({
                    'wallet_id': wallet_info[1],
                    'user_unique_number': wallet_info[0],
                    'available_balance': decimal.Decimal(balance['available_balance']),
                    'pending_received_balance': decimal.Decimal(balance['pending_received_balance']),
                })

        return wallets_data_list

    def delete_wallets():
        pass


def start_block_io_checker():
    path = 'https://blockchain.info/ticker'
    raw_response = requests.get(path)
    if raw_response.status_code == 200:
        response = raw_response.json()

        course = decimal.Decimal(response['USD']['last'])

        for api_key in [BLOCKIO_BITCOIN_API_KEY]:
            checker = BlockIOChecker('9169-2eea-75f4-7384', 'vintkor71084')
            data = checker.get_wallets_data()

            for i in data:
                if i['pending_received_balance'] > 0:
                    continue
                elif i['available_balance'] > 0:
                    wallet = BlockIOWallet.objects.get(
                        id=i['wallet_id'],
                        user__unique_number=i['user_unique_number'],
                    )
                    wallet.balance = i['available_balance']
                    wallet.balance_usd = i['available_balance'] * course
                    wallet.save(update_fields=('balance', 'balance_usd',))
                else:
                    continue
