from django.urls import path
from .import consumers

#define WebSocket URL patterns for chat functionality
websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]