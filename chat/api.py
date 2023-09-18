from rest_framework.generics import ListAPIView, ListCreateAPIView
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


# I wrote this code
# List all chat rooms
class ChatRoomView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


# List all chat messages
class ChatMessageView(ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

# end of code I wrote
