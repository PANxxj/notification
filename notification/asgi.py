import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from app.routing import websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification.settings')

django_asgi_application = get_asgi_application()

application= ProtocolTypeRouter(
    {
        'http':django_asgi_application,
        'websocket':
            URLRouter(websocket_urlpatterns)
        
    }
)