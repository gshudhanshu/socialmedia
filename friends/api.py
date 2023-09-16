from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import *
from .serializers import *


# I wrote this code
class ListFriends(ListCreateAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(user_id=user_id, accepted=True)


class ListFriendRequestsReceived(ListAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(friend=user_id, accepted=False)


class ListFriendRequestsSent(ListAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(user=user_id, accepted=False)

# end of code I wrote
