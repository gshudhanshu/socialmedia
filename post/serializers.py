from django.contrib.auth.models import User
from rest_framework import serializers

from userprofile.models import UserProfile
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
    user_details = UserSerializer(source='user', read_only=True)
    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # fields = '__all__'
        read_only_fields = ('user',)
        exclude = ('user',)

    def get_user_profile(self, obj):
        user = obj.user
        user_profile = UserProfile.objects.get(user=user)
        return {
            'profile_image': user_profile.profile_image.url,
        }

    def get_num_comments(self, obj):
        # Get the count of comments for the associated post
        return Comment.objects.filter(post=obj.post).count()


class LikeSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user',)
