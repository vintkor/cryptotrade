from .models import UsersFinanceHistory
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from django.db.transaction import atomic
from finance.models import BlockIOWallet, Purpose


def make_uuid():
    uuid = get_random_string(60)
    if UsersFinanceHistory.objects.filter(uuid=uuid).exists():
        return make_uuid()
    else:
        return uuid


def set_transaction_to_finance_history(
        amount,
        sender_purpose_id,
        recipient_purpose_id,
        uuid,
        sender_id=False,
        recipient_id=False
        ):
    """
    Сохранение транзакции в финансовой истории
    :param amount: Decimal.decimal
    :param sender_id: int
    :param recipient_id: int
    :param sender_purpose_id: int
    :param recipient_purpose_id: int
    :param uuid: string
    :return none
    """

    if amount < 0:
        raise ValueError(_('Сумма должно быть не меньше 0'))

    for i in (sender_id, recipient_id, sender_purpose_id, recipient_purpose_id):
        if isinstance(i, int):
            pass
        else:
            raise ValueError(_('Параметры sender_id, recipient_id и sender_purpose_id должны быть целочисленными'))

    ufh = UsersFinanceHistory()
    ufh.amount = -amount
    ufh.second_user_id = recipient_id
    ufh.purpose_id = sender_purpose_id
    ufh.uuid = uuid

    if sender_id:
        ufh.user_id = sender_id

    ufh.save()

    ufh2 = UsersFinanceHistory()
    ufh2.amount = amount
    ufh2.user_id = recipient_id
    ufh2.purpose_id = recipient_purpose_id
    ufh2.uuid = uuid

    if sender_id:
        ufh.second_user_id = sender_id

    ufh2.save()


def blockio_transfer_usd_to_user_balance():
    wallets = BlockIOWallet.objects.filter(
        is_done=False,
        balance_usd__gt=0,
    )

    sender_purpose = Purpose.objects.get(code=22)
    recipient_purpose = Purpose.objects.get(code=23)

    with atomic():

        for wallet in wallets:

            user = wallet.user
            user.balance = user.balance + wallet.balance_usd
            user.save(update_fields=('balance',))

            wallet.is_done = True
            wallet.save(update_fields=('is_done',))

            uuid = make_uuid()

            set_transaction_to_finance_history(
                amount=wallet.balance_usd,
                sender_purpose_id=sender_purpose.id,
                recipient_purpose_id=recipient_purpose.id,
                uuid=uuid,
                recipient_id=user.id,
            )
