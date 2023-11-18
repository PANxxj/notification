# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('dafd',)
        
        print(f"Connected: {self.scope}")
        id = self.scope['url_route']['kwargs']['pk']
        user=await database_sync_to_async(User.objects.get)(id=id)
        print('user',user)
        await self.create_user_channel(user)

    async def disconnect(self, close_code):
        user = self.scope['user']
        await self.close_user_channel(user)

    async def receive(self, text_data):
        user = self.scope['user']
        await self.send_user_notification(user, text_data)

    @database_sync_to_async
    def create_user_channel(self, user):
        user_channel = f"user_{user.id}"
        self.user_channel = user_channel
        print('self.channel_layer',self.channel_layer)
        async_to_sync(self.channel_layer.group_add)(user_channel, self.channel_name)

    @database_sync_to_async
    def close_user_channel(self, user):
        user_channel = getattr(self, 'user_channel', None)
        if user_channel:
            async_to_sync(self.channel_layer.group_discard)(user_channel, self.channel_name)

    @database_sync_to_async
    def send_user_notification(self, user, message):
        user_channel = f"user_{user.id}"
        async_to_sync(self.channel_layer.group_send)(
            user_channel,
            {
                'type': 'send_notification',
                'message': message,
            }
        )

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))


# User = get_user_model()

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print('Connected:', self.scope)
#         id = self.scope['url_route']['kwargs']['pk']
#         self.user = await database_sync_to_async(User.objects.get)(id=id)

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         message = text_data
#         await self.send_user_notification(message)

#     @database_sync_to_async
#     def send_user_notification(self, message):
#         data = {
#             'type': 'send_notification',
#             'message': message,
#         }
#         channel_name = f"user_{self.user.id}"
#         self.channel_layer.send(channel_name, data)

#     async def send_notification(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({'message': message}))
