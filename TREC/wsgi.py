"""
WSGI config for TREC project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/TheScouser/.virtualenvs/trec/src/TREC-modifed/'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TREC.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
