from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from chat.models import ChatRoom


# I wrote this code

class ChatView(LoginRequiredMixin, ListView):
    template_name = 'chat/chat.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return ChatRoom.objects.all()


class ChatRoomView(LoginRequiredMixin, ListView):
    template_name = 'chat/room.html'

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
        return chat_room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.get_queryset()
        return context

# end of code I wrote
