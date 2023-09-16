import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import *
from authentication.factories import UserFactory


# I wrote this code
class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.RelatedFactory(UserFactory, 'userprofile')

# end of code I wrote
