from django.urls import re_path

from messages_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/event/(?P<user_id>\w+)/$', consumers.EventConsumer.as_asgi()),
]