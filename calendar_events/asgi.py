"""
ASGI config for calendar_events project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from manage import get_secret

env = get_secret("ENVIRONMENT").capitalize()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calendar_events.config")
os.environ.setdefault("DJANGO_CONFIGURATION", env)

application = get_asgi_application()
