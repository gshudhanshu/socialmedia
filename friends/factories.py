import factory
from .models import *
from authentication.factories import UserFactory


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    friend = factory.SubFactory(UserFactory)
    accepted = True
