from django.urls import path
from . import views

# urlpatterns = [
#     path('chat', views.ChatView.as_view(), name='chat-view'),
#     path('chat/<str:room_name>', views.ChatRoomView.as_view(), name='chat-room-view')
# ]

urlpatterns = [
    path('chat', views.index_view, name='chat-index'),
    path('chat/<str:room_name>', views.room_view, name='chat-room'),
]
