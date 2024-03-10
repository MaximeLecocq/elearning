from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from users.models import User
from .models import ChatRoom, ChatMessage

# WebSocket consumer class for handling chat functionality asynchronously
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #establish WebSocket connection
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        #join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        #accept the WebSocket connection
        await self.accept()
    
    async def disconnect(self):
        #leave the room group
        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name
        )
        
    
    async def receive(self,text_data):
        #receive message from WebSocket
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        #send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room,
            }
        )
        #save the message asynchronously
        await self.save_message(username,room,message)
    
    async def chat_message(self,event):
        #receive message from room group
        message = event['message']
        username = event['username']
        room = event['room']

        #send message to WebSocket
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))

    @sync_to_async
    def save_message(self,username,room,message):
        #save message to the database asynchronously
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(slug=room)
        ChatMessage.objects.create(user=user,room=room,message_content=message)