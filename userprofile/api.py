from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import *


# I wrote this code

# API view to list all profiles
class ListProfiles(ListAPIView):
    serializer_class = UserProfileAPISerializer

    def get_queryset(self):
        return User.objects.all().select_related('userprofile')


# API view to view a single profile
class ViewProfile(RetrieveAPIView):
    serializer_class = UserProfileAPISerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all().filter(id=self.kwargs.get('user_id')).select_related('userprofile')

# end of code I wrote
