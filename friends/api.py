from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import *
from .serializers import *


# I wrote this code
# List all friends of a user
class ListFriends(ListCreateAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        friends = (Friend.objects.filter(user_id=user_id, accepted=True) |
                   Friend.objects.filter(friend_id=user_id, accepted=True))
        return friends


# List all friend requests received by a user
class ListFriendRequestsReceived(ListAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(friend=user_id, accepted=False)


# List all friend requests sent by a user
class ListFriendRequestsSent(ListAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(user=user_id, accepted=False)

# end of code I wrote
