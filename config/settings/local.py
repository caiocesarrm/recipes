from .base import *  # noqa
from .base import env

DEBUG = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.DummyCache",
        "LOCATION": "",
    }
}
