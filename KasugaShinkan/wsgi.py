"""
WSGI config for KasugaShinkan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import site
import sys
import os

from django.core.wsgi import get_wsgi_application

site.addsitedir("/home/ubuntu/Django/env/lib/python3.6/site-packages")
sys.path.append("/home/ubuntu/Django/KasugaShinkan")
sys.path.append("/home/ubuntu/Django/KasugaShinkan/KasugaShinkan")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KasugaShinkan.settings')

application = get_wsgi_application()
