from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Friend


# I wrote this code
# Serializer for the Friend model
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

        # Check if user is sending a friend request to himself
        if user == friend:
            raise serializers.ValidationError(
                {'message': 'You cannot send a friend request to yourself.', 'request_sent_or_exist': False,
                 'user': user, 'friend': friend})

        request_exists = Friend.objects.filter(user=user, friend=friend).exists()
        reverse_request_exists = Friend.objects.filter(user=friend, friend=user).exists()

        # Check if a friend request already exists from both sides
        # If a friend request already exists, raise a validation error
        if request_exists or reverse_request_exists:
            raise serializers.ValidationError(
                {'message': 'Friend request already exists.', 'request_sent_or_exist': True, 'user': user,
                 'friend': friend})
        else:
            friend_request = Friend(user=user, friend=friend)
            friend_request.save()

    def accept_request(self):
        user = self.validated_data['user']
        friend = self.validated_data['friend']

        # Check if a friend request exists
        friend_request = Friend.objects.filter(id=self.data['id'], accepted=False).first()
        if friend_request:
            friend_request.accept()
            return {'message': 'Friend request accepted.',
                    'request_accepted': True, **self.data}
        else:
            return {'message': 'Friend request does not exist.',
                    'request_accepted': False, **self.data}

    def decline_request(self):
        user = self.validated_data['user']
        friend = self.validated_data['friend']

        # Check if a friend request exists
        friend_request = Friend.objects.filter(id=self.data['id'], accepted=False).first()
        if friend_request:
            friend_request.decline()
            return {'message': 'Friend request declined.',
                    'request_declined': True, **self.data}
        else:
            return {'message': 'Friend request does not exist.',
                    'request_declined': False, **self.data}

    def cancel_request(self):
        user = self.validated_data['user']
        friend = self.validated_data['friend']

        # Check if a friend request exists
        friend_request = Friend.objects.filter(id=self.data['id']).first()
        if friend_request:
            friend_request.cancel()
            return {'message': 'Friend request cancelled.',
                    'request_cancelled': True, **self.data}
        else:
            return {'message': 'Friend request does not exist.',
                    'request_cancelled': False, **self.data}

    def remove_friend(self):
        user = self.validated_data['user']
        friend = self.validated_data['friend']

        # Check if a friend request exists
        friend_request = Friend.objects.filter(id=self.data['id']).first()
        if friend_request:
            friend_request.remove()
            return {'message': 'Friend removed.',
                    'friend_removed': True, **self.data}
        else:
            return {'message': 'Friend request does not exist.',
                    'friend_removed': False, **self.data}


#  REST API Views serializers
class ListFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"

# end of code I wrote
