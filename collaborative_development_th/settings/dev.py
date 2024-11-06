import os

from .base import *  # noqa: F403
from .utils import strtobool

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-)vqqtqvm9rz)4*&5on*^ezhu7%xt1$osmjhn38%afuzpb2ct0!",
)

DEBUG = strtobool(os.getenv("DEBUG", "y"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        # "app_name": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        # }
    },
}

if strtobool(os.getenv("DEBUG_SQL", "n")):
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
    }
