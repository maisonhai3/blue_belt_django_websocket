from django.urls import re_path
from .consumer import MessageConsumer


websocket_urlpatterns = [
    re_path(r'ws/message/$', MessageConsumer.as_asgi()),
]
