from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from functools import wraps
import time

from home import utils as home_utils
from movies.models import Movies

user = get_user_model()

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
        parser.add_argument('count',type=int,default=10,nargs='?')
        parser.add_argument('--movies',action='store_true',default=False,)
        parser.add_argument('--users',action='store_true',default=False,)
        parser.add_argument('--show-total',action='store_true',default=False,)

    @timer
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')
        if load_movies:
            movie_dataset = home_utils.load_movie_data(limit=count)
            movies_sealize = [Movies(**x) for x in movie_dataset]
            movies_bulk_create = Movies.objects.bulk_create(movies_sealize, ignore_conflicts=True)
            print(f"New movies: {len(movies_bulk_create)}")
            if show_total:
                print(f"Total movies: {Movies.objects.count()}")
        if generate_users:
            profiles = home_utils.get_fake_profiles(count=count)
            new_user = []
            for profile in profiles:
                new_user.append(
                    user(**profile)
                )
            user_bulk = user.objects.bulk_create(new_user, ignore_conflicts=True)
            print(f'New user : {len(user_bulk)} added successfully')
            if show_total:
                print(f'The total users: {user.objects.count()}')
