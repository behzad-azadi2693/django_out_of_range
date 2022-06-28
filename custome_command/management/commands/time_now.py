from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

class Command(BaseCommand):
    help = 'Display current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write(f'It is now {time}')
