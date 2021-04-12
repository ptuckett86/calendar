import os

from os.path import join

from manage import get_secret

from .common import Common


class Prod(Common):
    DEBUG = True
    DOMAIN = "ec2-18-223-15-184.us-east-2.compute.amazonaws.com"
#    Common.ALLOWED_HOSTS += ["18.223.15.184", "ec2-18-223-15-184.us-east-2.compute.amazonaws.com", "ec2-3-19-221-117.us-east-2.compute.amazonaws.com", "https://script.google.com"]
    PROTOCOL = "http"
    CORS_ALLOW_HEADERS = (
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "range",
    )
    CORS_ALLOW_CREDENTIALS = True
    SECURE_HSTS_SECONDS = 60
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", PROTOCOL)
    CSRF_TRUSTED_ORIGINS = [DOMAIN]
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    DEFAULT_FROM_EMAIL = "Test <noreply@gmail.com>"
    CORS_ALLOW_ALL_ORIGINS = True
