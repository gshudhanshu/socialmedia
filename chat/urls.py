from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('chat', views.ChatView.as_view(), name='chat-index'),
    path('chat/<str:room_name>', views.ChatRoomView.as_view(), name='chat-room'),

    # REST API URLS
    path('api/chat', api.ChatRoomView.as_view(), name='api-chat-view'),
    path('api/chat/<str:room_name>', api.ChatMessageView.as_view(), name='api-chat-room-view'),
]
