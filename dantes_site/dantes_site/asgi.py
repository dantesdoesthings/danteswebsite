"""
ASGI config for dantes_site project.
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dantes_site.settings')

if settings.DEBUG:
    application = ASGIStaticFilesHandler(get_asgi_application())
else:
    application = get_asgi_application()
