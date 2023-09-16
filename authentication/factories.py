import factory
from django.contrib.auth.models import User
from .models import *


# I wrote this code
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
# end of code I wrote
