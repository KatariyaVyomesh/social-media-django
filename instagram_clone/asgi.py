# instagram_clone/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import instaclone.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_clone.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            instaclone.routing.websocket_urlpatterns
        )
    ),
})