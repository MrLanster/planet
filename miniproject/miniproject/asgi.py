"""
ASGI config for miniproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# asgi.py
import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniproject.settings')

# Get the Django application
django_application = get_asgi_application()

# Wrap the application in an asynchronous function
async def application(scope, receive, send):
    await django_application(scope, receive, send)
