from django.core.management.base import BaseCommand
from django.contrib.auth.models import User



class Command(BaseCommand):
    help = 'create user for applications'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='name for username')
        parser.add_argument('password', type=str, help='password for user')

        parser.add_argument('-a', '--admin', action='store_true', help='create user admin accounts')
        parser.add_argument('-p', '--prefix', type=str, nargs=1, help='create user admin accounts')


    def handle(self, *args, **kwargs):
        name = kwargs['name']
        password = kwargs['password']
        admin = kwargs['admin']
        prefix = kwargs['prefix'][0]

        user = User.objects.filter(username=name).exists()

        if user:
            self.stdout.write(self.style.ERROR('username already exists.'))

        elif admin:
            if prefix:
                username = f'{prefix}_{name}'
                User.objects.create_superuser(username=username, email='', password=password)
                self.stdout.write(self.style.SUCCESS(f'user admin with username {username} with password {password} created'))
    
            else:
                User.objects.create_superuser(username=name, email='', password=password)
                self.stdout.write(self.style.SUCCESS(f'user admin with username {name} with password {password} created'))

        else:
            if prefix:
                username = f'{prefix}_{name}'
                User.objects.create_user(username=username, email='', password=password)
                self.stdout.write(self.style.SUCCESS(f'user with username {username} with password {password} created'))
    
            else:
                User.objects.create_user(username=name, email='', password=password)
                self.stdout.write(self.style.SUCCESS(f'user with username {name} with password {password} created'))

