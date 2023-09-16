from django.db.models import Count, Exists, OuterRef
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *


class ListProfiles(ListAPIView):
    serializer_class = UserProfileAPISerializer

    def get_queryset(self):
        return User.objects.all().select_related('userprofile')


class ViewProfile(RetrieveAPIView):
    serializer_class = UserProfileAPISerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all().filter(id=self.kwargs.get('user_id')).select_related('userprofile')
