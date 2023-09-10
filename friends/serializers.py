from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from authentication.models import UserProfile
from .models import Friend


class FriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    friend = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Friend
        fields = '__all__'

    def create_request(self):
        # Check if a friend request already exists from both sides
        user = self.validated_data['user']
        friend = self.validated_data['friend']

        if user == friend:
            raise serializers.ValidationError(
                {'message': 'You cannot send a friend request to yourself.', 'user': user, 'friend': friend})

        request_exists = Friend.objects.filter(user=user, friend=friend).exists()
        reverse_request_exists = Friend.objects.filter(user=friend, friend=user).exists()

        if request_exists or reverse_request_exists:
            raise serializers.ValidationError(
                {'message': 'Friend request already exists.', 'user': user, 'friend': friend})
        else:
            friend_request = Friend(user=user, friend=friend)
            friend_request.save()

    def accept_request(self):
        # Check if a friend request exists
        friend_request = Friend.objects.filter(user=self.friend, friend=self.user, accepted=False).first()
        if friend_request:
            friend_request.accept()
            return JsonResponse({'message': 'Friend request accepted.'}, status=200)
        else:
            return JsonResponse({'message': 'Friend request does not exist.'}, status=400)

    def decline_request(self):
        # Check if a friend request exists
        friend_request = Friend.objects.filter(user=self.friend, friend=self.user, accepted=False).first()
        if friend_request:
            friend_request.decline()
            return JsonResponse({'message': 'Friend request declined.'}, status=200)
        else:
            return JsonResponse({'message': 'Friend request does not exist.'}, status=400)

    def cancel_request(self):
        # Check if a friend request exists
        friend_request = Friend.objects.filter(user=self.user, friend=self.friend, accepted=False).first()
        if friend_request:
            friend_request.cancel()
            return JsonResponse({'message': 'Friend request cancelled.'}, status=200)
        else:
            return JsonResponse({'message': 'Friend request does not exist.'}, status=400)
