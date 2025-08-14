# instaclone/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.receiver_username = self.scope['url_route']['kwargs']['username']
        self.sender = self.scope['user']
        
        if not self.sender.is_authenticated:
            self.close()
            return

        try:
            self.receiver = User.objects.get(username=self.receiver_username)
        except User.DoesNotExist:
            self.close()
            return
        
        # Sort usernames to create consistent room name
        user1, user2 = sorted([self.sender.username, self.receiver_username])
        self.room_name = f'chat_{user1}_{user2}'
        self.room_group_name = f'chat_{user1}_{user2}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            message_type = text_data_json.get('type', 'message')

            # Only save if it's a message (not typing indicator etc)
            if message_type == 'message':
                saved_message = self.save_message(self.sender, self.receiver, message)
                
                if not saved_message:
                    self.send(text_data=json.dumps({
                        'error': 'Failed to save message'
                    }))
                    return

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.sender.username,
                    'timestamp': str(saved_message.timestamp) if saved_message else str(timezone.now())
                }
            )
        except Exception as e:
            print(f"Error processing message: {e}")

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp,
            'type': 'message'
        }))

    def save_message(self, sender, receiver, text):
        try:
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                text=text
            )
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            return None