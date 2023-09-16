from django.shortcuts import render
from django.views.generic import ListView

from chat.models import ChatRoom


# Create your views here.

# Create class for chat view with rooms
class ChatView(ListView):
    template_name = 'chat/chat.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return ChatRoom.objects.all()


# Create class for chat room view
class ChatRoomView(ListView):
    template_name = 'chat/room.html'

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
        return chat_room
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.get_queryset()
        return context


def index_view(request):
    return render(request, 'chat/chat.html', {
        'rooms': ChatRoom.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {
        'room': chat_room,
    })
