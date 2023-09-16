import factory
from .models import ChatRoom, ChatMessage


class ChatRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatRoom

    name = factory.Faker('name')


class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage

    room_name = factory.SubFactory(ChatRoomFactory)
    user = factory.Faker('word')
    message = factory.Faker('sentence')
