# urls.py
from django.urls import path
from .views import trigger_notification

urlpatterns = [
    # ... other paths
    path('api/trigger-notification/', trigger_notification, name='trigger_notification'),
]
