import factory
from django.contrib.auth.models import User
from .models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    friend = factory.SubFactory(UserFactory)
    accepted = True
