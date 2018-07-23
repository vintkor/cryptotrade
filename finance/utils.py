from .models import UsersFinanceHistory
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string


def make_uuid():
    uuid = get_random_string(60)
    if UsersFinanceHistory.objects.filter(uuid=uuid).exists():
        return make_uuid()
    else:
        return uuid


def set_transaction_to_finance_history(amount, sender_id, recipient_id, sender_purpose_id, recipient_purpose_id, uuid):
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

    ufh = UsersFinanceHistory(
        amount=-amount,
        user_id=sender_id,
        second_user_id=recipient_id,
        purpose_id=sender_purpose_id,
        uuid=uuid,
    )
    ufh.save()

    ufh2 = UsersFinanceHistory(
        amount=amount,
        user_id=recipient_id,
        second_user_id=sender_id,
        purpose_id=recipient_purpose_id,
        uuid=uuid,
    )
    ufh2.save()
