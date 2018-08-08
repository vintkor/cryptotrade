from django.core.management.base import BaseCommand, CommandError
from awards.utils import start_point_awadr


class Command(BaseCommand):
    help = 'running Point award'

    def handle(self, *args, **option):
        print()
        print('------->', self.help, '<-------')
        print()
        start_point_awadr()
