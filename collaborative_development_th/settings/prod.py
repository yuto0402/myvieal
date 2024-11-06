import os

from .base import *  # noqa: F403
from .utils import split_to_list

# Security

SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("X-Forwarded-Proto", "https")

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN")
CSRF_TRUSTED_ORIGINS = split_to_list(os.getenv("CSRF_TRUSTED_ORIGINS", ""))

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "simple": {
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 format
            "format": "%(asctime)s: %(levelname)s: %(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file_error": {
            "class": "logging.FileHandler",
            "filename": os.getenv("ERROR_LOG_FILE", "/var/log/collaborative_development_th/error.log"),
            "formatter": "simple",
            "level": "ERROR",
        },
        "file_info": {
            "class": "logging.FileHandler",
            "filename": os.getenv("INFO_LOG_FILE", "/var/log/collaborative_development_th/info.log"),
            "formatter": "simple",
            "level": "INFO",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "include_html": True,
            "level": "ERROR",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        # "app_name": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        # }
    },
}

# Storages

AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-1")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Boto3Storage",
        "OPTIONS": {
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "collaborative_development_th.storage.StaticStorage",
        "OPTIONS": {
            "location": "static",
        },
    },
}
