from settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_mathbuddy",
        "USER": "userone",
        "PASSWORD": "12345",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
