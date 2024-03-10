from django.shortcuts import render
from .models import ChatRoom,ChatMessage

#render the index page with a list of all available chat rooms
def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html',{'chatrooms':chatrooms})

#render the chat room page with the specified slug
def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=chatroom)[0:30]
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':messages})