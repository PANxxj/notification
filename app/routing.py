from django.urls import path
from .consumers import NotificationConsumer


websocket_urlpatterns = [
    path('ws/notifications/<int:pk>', NotificationConsumer.as_asgi()),
]