from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

user = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(f"there are {user.objects.count()} users")

