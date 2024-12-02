from django.urls import path, re_path
from app01.consumers import ChatConsumer


websocket_urlpatterns = [
    # xxxxxx/room/x1
    re_path('api//(\d+)',ChatConsumer.as_asgi()),
]