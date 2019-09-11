import random
from .models import ScrumyGoals
from django.core.exceptions import ObjectDoesNotExist


def generate_unique_random_int(a, b):
    is_not_unique = True

    while is_not_unique:
        random_int = random.randint(a, b)
        try:
            ScrumyGoals.objects.get(pk=random_int)
        except ObjectDoesNotExist:
            return random_int
