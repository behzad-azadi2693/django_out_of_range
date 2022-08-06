from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'remove user of db'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int, help='ids of users for delete')


    def handle(self, *args, **kwargs):
        user_ids = kwargs['user_id']

        for user_id in user_ids:
            try:
                user = User.objects.get(pk = user_id)
                user.delete()
                self.stdout.write(self.style.SUCCESS(f'user with id {user_id} delte'))

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'user with id {user_id} not found'))
