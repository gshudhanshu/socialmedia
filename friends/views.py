from django.contrib.auth.models import User
from django.db.models import F, Q
from django.views.generic import ListView
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
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
        serializer = self.get_serializer(data={'user': user, 'friend': friend})
        serializer.is_valid(raise_exception=True)
        serializer.create_request()
        return Response({'message': 'Friend request sent.', 'request_sent_or_exist': True, **serializer.data},
                        status=200)


class ListFriends(ListView):
    model = Friend
    template_name = 'friends/friends.html'
    context_object_name = 'friends'

    def get_friend_requests_sent(self):
        friend_requests_sent = Friend.objects.filter(user_id=self.request.user.id, accepted=False).select_related(
            'friend__userprofile')
        return friend_requests_sent

    def get_friend_request_received(self):
        friend_requests_received = Friend.objects.filter(friend_id=self.request.user.id, accepted=False).select_related(
            'user__userprofile')
        return friend_requests_received

    def get_queryset(self):
        #     get all users excluding logged in user and users who have sent or received friend requests
        queryset = User.objects.exclude(id=self.request.user.id)
        queryset = queryset.exclude(
            id__in=Friend.objects.filter(user_id=self.request.user.id).values_list('friend_id', flat=True))
        queryset = queryset.exclude(
            id__in=Friend.objects.filter(friend_id=self.request.user.id).values_list('user_id', flat=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['friend_requests_received'] = self.get_friend_request_received()
        context['friend_requests_sent'] = self.get_friend_requests_sent()
        print(context['friends'])
        return context


class AcceptOrDeclineCancelFriendAPI(RetrieveUpdateDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        if self.request.data.get('user') is not None:
            user = get_object_or_404(User, username=self.request.data.get('user'))
        else:
            user = self.request.user
        friend = get_object_or_404(User, id=self.request.data.get('friend_id'))
        if self.request.data.get('request_type') == 'cancel':
            friend_request = get_object_or_404(Friend, user=user, friend=friend)
        else:
            friend_request = get_object_or_404(Friend, user=friend, friend=user)
        return friend_request

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if self.request.data.get('request_type') == 'accept' or self.request.data.get('request_type') == 'decline':
            serializer = self.get_serializer(friend_request, data={'user': friend_request.friend,
                                                                   'friend': friend_request.user})
        else:
            serializer = self.get_serializer(friend_request, data={'user': friend_request.user,
                                                                   'friend': friend_request.friend})

        serializer.is_valid(raise_exception=True)
        global result
        if self.request.data.get('request_type') == 'accept':
            result = serializer.accept_request()
        elif self.request.data.get('request_type') == 'decline':
            result = serializer.decline_request()
        elif self.request.data.get('request_type') == 'cancel':
            result = serializer.cancel_request()
        return Response(result, status=200)
