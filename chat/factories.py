import factory
from .models import ChatRoom, ChatMessage
from authentication.factories import UserFactory


# I wrote this code
class ChatRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatRoom

    name = factory.Faker('word')


class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage

    room_name = factory.SubFactory(ChatRoomFactory)
    user = factory.SubFactory(UserFactory)
    message = factory.Faker('sentence')

# end of code I wrote
