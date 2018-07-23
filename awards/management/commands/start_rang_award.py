from django.core.management.base import BaseCommand, CommandError
from awards.utils import RangAwardRunner
from user_profile.models import User


class Command(BaseCommand):
    help = 'running Rang award'

    def handle(self, *args, **option):
        print(self.help)
        print('-'*90)

        user = User.objects.get(login='vintkor')
        runner = RangAwardRunner(user)
        runner.check_user()
