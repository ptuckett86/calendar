from manage import get_secret

from .common import Common


class Dev(Common):
    DEBUG = True
    PROTOCOL = "http"
    DOMAIN = "localhost"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "paulltuckett@gmail.com"
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = ["http://localhost:4200", "http://localhost:4300"]
