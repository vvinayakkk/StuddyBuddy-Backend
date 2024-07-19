# room/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from authentication.models import User
from django.conf import settings
import jwt
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        token = text_data_json.get('token')

        user, _ = self.get_user_from_token(token)
        if not user:
            return

        room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
        message_obj = await database_sync_to_async(Message.objects.create)(user=user, room=room, content=message)
        # Broadcast message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user.username,
                'message': message,
                'timestamp': message_obj.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        user = event['user']
        message = event['message']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message,
            'timestamp': timestamp,
        }))

    def get_user_from_token(self, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('id')
            if user_id:
                return User.objects.get(id=user_id), None
        except Exception as e:
            return None, str(e)
        return None, "Invalid token"
