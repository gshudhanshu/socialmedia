from rest_framework import serializers
from .models import ChatRoom, ChatMessage


# I wrote this code
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

# end of code I wrote
