from finance.models import Purpose
from .models import RangAward
from linear_tree.models import LinearTree
from user_profile.models import User
from django.db.transaction import atomic
from finance.utils import set_transaction_to_finance_history, make_uuid


class RangAwardRunner:

    def __init__(self, user, rules):
        self._user = user
        self._volume = user.volume
        self._lines_volume = 0
        self._include_rang_count = 0
        self._rules = rules
        self._linear_nodes_for_count = []

    def _set_linear_nodes_for_count(self, lines):
        linear_user_node = LinearTree.objects.get(user=self._user)
        level = lines + linear_user_node.level
        queryset = linear_user_node.get_descendants().filter(level__lte=level).select_related('user')
        for node in queryset:
            self._linear_nodes_for_count.append({
                'node': node,
                'volume': node.user.volume,
            })

    def _get_lines_volume(self, lines):
        self._set_linear_nodes_for_count(lines)
        lines_volume = sum([i['volume'] for i in self._linear_nodes_for_count])
        self._lines_volume = lines_volume

    def _get_include_rang_count(self, rang):
        include_rang_count = 0

        for i in self._linear_nodes_for_count:
            if i['node'].user.rang == rang:
                include_rang_count += 1

        self._include_rang_count = include_rang_count

    def check_user(self):
        for rule in self._rules:
            print('----------------', rule['object'].title, '----------------')

            # Проверка объёма
            if self._volume < rule.get('volume', 0):
                print('Проверка объёма', self._volume)
                continue

            # Проверка объёма в линиях
            self._get_lines_volume(rule.get('max_lines', 0))
            if self._lines_volume < rule.get('lines_volume', 0):
                print('Проверка объёма в линиях', self._lines_volume)
                continue

            # Проверка количества ранговых партнёров
            self._get_include_rang_count(rule.get('object'))
            if self._include_rang_count < rule.get('include_rang_count'):
                print('Проверка количества ранговых партнёров', self._include_rang_count)
                continue

            print(rule['object'])
            return True, rule.get('object')
        return False, 0


def get_rules():
    rules = []
    for item in RangAward.objects.all():
        rules.append({
            'object': item,
            'volume': item.volume,
            'max_lines': item.max_lines,
            'lines_volume': item.lines_volume,
            'include_rang': item.include_rang,
            'include_rang_count': item.include_rang_count,
        })
    return rules


def start_rang_award_runner():
    users = User.objects.select_related('rang').filter(is_in_tree=True).iterator()

    rules = get_rules()
    system_balance = User.objects.get(login='SYSTEM_BALANCE')
    sender_purpose = Purpose.objects.get(code=12)
    recipient_purpose = Purpose.objects.get(code=13)

    for user in users:
        print('---->', user.unique_number)
        runner = RangAwardRunner(user, rules)
        status, rang = runner.check_user()

        if status:
            with atomic():

                if user.rang != rang:
                    user.rang = rang
                    user.balance += rang.bonus
                    user.save(update_fields=('balance', 'rang'))

                    set_transaction_to_finance_history(
                        amount=rang.bonus,
                        sender_id=system_balance.id,
                        recipient_id=user.id,
                        sender_purpose_id=sender_purpose.id,
                        recipient_purpose_id=recipient_purpose.id,
                        uuid=make_uuid(),
                    )
