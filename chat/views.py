from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.

class ChatView(ListView):
    template_name = 'chat/chat.html'
    context_object_name = 'chat'
