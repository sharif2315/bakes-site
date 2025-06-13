from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG  # or just False
    }
}