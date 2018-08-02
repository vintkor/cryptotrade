from finance.models import Purpose
from .models import RangAward, MultiLevelBonus, MultiLevelBonusHistory, RangAwardHistory
from linear_tree.models import LinearTree
from user_profile.models import User
from django.db.transaction import atomic
from finance.utils import set_transaction_to_finance_history, make_uuid
import decimal
from prettytable import PrettyTable


class RangAwardRunner:

    def __init__(self, user, rules):
        self._user = user
        self._volume = user.volume
        self._lines_volume = 0
        self._include_rang_count = 0
        self._rules = rules

    def _set_linear_nodes_for_count(self, lines):
        linear_user_node = LinearTree.objects.get(user=self._user)
        level = lines + linear_user_node.level
        queryset = linear_user_node.get_descendants().filter(level__lte=level).select_related('user')
        self._linear_nodes_for_count = []
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
        self._set_linear_nodes_for_count(rang.max_lines)
        include_rang_count = 0

        for i in self._linear_nodes_for_count:
            if i['node'].user.rang == rang:
                include_rang_count += 1

        self._include_rang_count = include_rang_count

    def check_user(self):
        log = PrettyTable([
            "current rule",
            "user",
            "volume own sum",
            "volume lines sum",
            "count rang partners",
            "new rang",
        ])

        for rule in self._rules:

            log.add_row([
                rule['object'].title,
                self._user.unique_number,
                '{} / {}'.format(rule['object'].volume, self._volume),
                '',
                '',
                '',
            ])

            # Проверка объёма
            if self._volume < rule.get('volume', 0):
                continue

            log.add_row([
                rule['object'].title,
                self._user.unique_number,
                '{} / {}'.format(rule['object'].volume, self._volume),
                '{} / {}'.format(rule['object'].lines_volume, self._lines_volume),
                '',
                '',
            ])

            # Проверка объёма в линиях
            self._get_lines_volume(rule.get('max_lines', 0))
            if self._lines_volume < rule.get('lines_volume', 0):
                continue

            # Проверка количества ранговых партнёров
            self._get_include_rang_count(rule.get('object'))

            log.add_row([
                rule['object'].title,
                self._user.unique_number,
                '{} / {}'.format(rule['object'].volume, self._volume),
                '{} / {}'.format(rule['object'].lines_volume, self._lines_volume),
                '({}) {} / {}'.format(rule['object'].include_rang, rule['object'].include_rang_count, self._include_rang_count),
                '',
            ])

            if self._include_rang_count < rule.get('include_rang_count'):
                continue

            log.add_row([
                rule['object'].title,
                self._user.unique_number,
                '{} / {}'.format(rule['object'].volume, self._volume),
                '{} / {}'.format(rule['object'].lines_volume, self._lines_volume),
                '({}) {} / {}'.format(rule['object'].include_rang, rule['object'].include_rang_count, self._include_rang_count),
                rule['object'],
            ])
            print(log.get_string())
            return True, rule.get('object'), log.get_html_string(), self._user.id
        return False, 0, log.get_html_string(), self._user.id


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
    """
    Просчёт рангового бонуса
    """
    users = User.objects.select_related('rang').filter(is_in_tree=True).iterator()

    rules = get_rules()
    system_balance = User.objects.get(login='SYSTEM_BALANCE')
    sender_purpose = Purpose.objects.get(code=12)
    recipient_purpose = Purpose.objects.get(code=13)

    for user in users:
        runner = RangAwardRunner(user, rules)
        status, rang, log, user_id = runner.check_user()

        if status:
            with atomic():

                if user.rang != rang:
                    if rang.bonus > 0:
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

        rah = RangAwardHistory()
        rah.user_id = user_id
        rah.text = log
        rah.save()


def start_multi_level_bonus_runner(user_id, amount, package_history_id):
    """
    просчё многоуровневого бонуса
    :param user_id: int
    :param amount: int
    :param package_history_id: int
    """
    l_user = LinearTree.objects.get(user_id=user_id)
    amount = decimal.Decimal(amount)

    bonuses = dict()
    for bonus in MultiLevelBonus.objects.select_related('rang').all():
        bonuses[bonus.rang] = {
            'level_1': bonus.bonus_for_line_1,
            'level_2': bonus.bonus_for_line_2,
            'level_3': bonus.bonus_for_line_3,
            'level_4': bonus.bonus_for_line_4,
            'level_5': bonus.bonus_for_line_5,
            'level_6': bonus.bonus_for_line_6,
            'level_7': bonus.bonus_for_line_7,
            'level_8': bonus.bonus_for_line_8,
            'level_9': bonus.bonus_for_line_9,
            'level_10': bonus.bonus_for_line_10,
        }

    x = PrettyTable(["User", "Rang", "level_to_initiator", "percent", "bonus"])

    l_user_level = l_user.level
    levels = [l_user_level - i for i in range(1, 11) if l_user_level - i >= 0]
    ancestors = l_user.get_ancestors().prefetch_related('user').filter(level__in=levels)
    candidates = dict()
    for ancestor in ancestors:
        if ancestor.user.rang:
            ancestor_user = ancestor.user
            level_to_initiator = l_user_level - ancestor.level
            ancestor_rang = ancestor_user.rang
            percent = sum([v for k, v in bonuses[ancestor_rang].items() if k == 'level_{}'.format(level_to_initiator)])
            bonus = (amount * percent) / 100

            candidates[ancestor_user] = dict()
            candidates[ancestor_user]['bonus'] = bonus

            x.add_row([
                ancestor_user.unique_number,
                ancestor_rang,
                level_to_initiator,
                str(percent),
                bonus,
            ])

    system_balance = User.objects.get(login='SYSTEM_BALANCE')
    sender_purpose = Purpose.objects.get(code=16)
    recipient_purpose = Purpose.objects.get(code=17)

    with atomic():
        multi_level_bonus_history = MultiLevelBonusHistory(
            package_history_id=package_history_id,
            text=x.get_html_string(),
        )
        multi_level_bonus_history.save()

        for candidate, bonus in candidates.items():
            if bonus['bonus'] > 0:
                candidate.balance += bonus['bonus']
                candidate.save(update_fields=('balance',))

                uuid = make_uuid()

                set_transaction_to_finance_history(
                    amount=bonus['bonus'],
                    sender_id=system_balance.id,
                    recipient_id=candidate.id,
                    sender_purpose_id=sender_purpose.id,
                    recipient_purpose_id=recipient_purpose.id,
                    uuid=uuid,
                )


