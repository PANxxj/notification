# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .authentication import MultiTokenAuthentication

User = get_user_model()

@api_view(['GET'])
@authentication_classes([MultiTokenAuthentication])
@permission_classes([IsAuthenticated])
def trigger_notification(request):
    user = request.user
    message = f"Notification triggered from API method. and the user {user}"

    # Send the message to the user's WebSocket consumer
    channel_layer = get_channel_layer()
    user_channel = f"user_{user.id}"
    
    async_to_sync(channel_layer.group_send)(
        user_channel,
        {
            'type': 'send_notification',
            'message': message,
        }
    )

    return Response({"message": "Notification triggered successfully"})
