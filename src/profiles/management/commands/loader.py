from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.utils import get_fake_profiles

user = get_user_model()

from functools import wraps
import time

def timer(func):
    """helper function to estimate view execution time"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)
        
        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__, 
            duration
            ))
        return result
    return wrapper

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            default=10,
            nargs='?'
            )
        parser.add_argument(
            '--show-total',
            action='store_true',
            default=False,
        )
    @timer
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        profiles = get_fake_profiles(count=count)
        new_user = []
        for profile in profiles:
            new_user.append(
                user(**profile)
            )
        user_bulk = user.objects.bulk_create(new_user, ignore_conflicts=True)
        print(f'New user : {len(user_bulk)} added successfully')
        if show_total:
            print(f'The total users: {user.objects.count()}')
