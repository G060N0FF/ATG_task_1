from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\d+-\d+)/$', consumers.ChatConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'wss/chat/(?P<room_name>\d+-\d+)/$', consumers.ChatConsumer),
    re_path(r'wss/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
