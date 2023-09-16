import factory
from .models import *
from authentication.factories import UserFactory


# I wrote this code
# Friend factory for generating fake data
class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    friend = factory.SubFactory(UserFactory)
    accepted = True

# end of code I wrote
