import os
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(env_variable):
    try:
        return os.environ.get(env_variable)
    except KeyError:
        error_msg = f'{env_variable} not found.'
        raise ImproperlyConfigured(error_msg)