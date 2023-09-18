"""
ASGI config for matchingapp_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from matchingapp_project.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchingapp_project.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # WSGIアプリケーション
    "websocket": websocket_urlpatterns,  # WebSocketのルーティング定義を指定
})
