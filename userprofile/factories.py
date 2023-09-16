import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import *
from authentication.factories import UserFactory


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.RelatedFactory(UserFactory, 'userprofile')
