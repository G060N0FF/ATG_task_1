import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Notification, ChatGroup
from django.contrib.auth.models import User

import base64
from django.core.files.base import ContentFile


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        self.user.profile.is_online = True
        self.user.profile.save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        self.user.profile.is_online = False
        self.user.profile.save()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        image = text_data_json['dataURL']

        self.user = self.scope["user"]

        if message:
            new_message = Message.objects.create(user=self.user, text=message, group=self.room_name)
        if image:
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            new_message = Message.objects.create(user=self.user, group=self.room_name, image=data)

        new_msg = [self.user.username, message, str(new_message.date_time).split('.')[0], new_message.pk, new_message.image.url] if new_message.image else [self.user.username, message, str(new_message.date_time).split('.')[0], new_message.pk]

        # send a notification
        if '_' in self.room_name:
            ids = self.room_name.split('_')
            for id in ids:
                temp_user = User.objects.get(pk=id)
                new_noti = Notification(sender=self.room_name, receiver=temp_user)
                new_noti.save()
        elif self.room_name != 'lobby':
            for temp_user in ChatGroup.objects.get(name=self.room_name).users.all():
                new_noti = Notification(sender=self.room_name, receiver=temp_user)
                new_noti.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_msg
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
