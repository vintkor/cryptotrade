from django.core.management.base import BaseCommand, CommandError
from awards.utils import start_rang_award_runner
from user_profile.models import User


class Command(BaseCommand):
    help = 'running Rang award'

    def handle(self, *args, **option):
        print()
        print('------->', self.help, '<-------')
        print()
        start_rang_award_runner()
