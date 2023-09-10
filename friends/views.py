from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .models import Friend


class AddFriendAPI(ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if self.request.data.get('user') is not None:
            user = get_object_or_404(User, username=self.request.data.get('user'))
        else:
            user = self.request.user
        friend = get_object_or_404(User, id=self.request.data.get('friend_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = user
        serializer.validated_data['friend'] = friend
        serializer.create_request()
        return Response({'message': 'Friend request sent.', **serializer.data}, status=200)
