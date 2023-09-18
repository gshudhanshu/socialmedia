from django.contrib.auth.models import User
from rest_framework import serializers

from userprofile.models import UserProfile
from .models import Post, Comment, Like


# I wrote this code

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    num_likes = serializers.IntegerField(read_only=True)
    num_comments = serializers.IntegerField(read_only=True)
    user_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# Serializer for the create post
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


# Serializer for the user model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Serializer for the comment model
class CommentSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
    user_details = UserSerializer(source='user', read_only=True)
    num_comments = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ('user',)
        # exclude = ('user',)

    def get_user_profile(self, obj):
        user = obj.user
        user_profile = UserProfile.objects.get(user=user)
        return {
            'profile_image': user_profile.profile_image.url,
        }

    # Get the count of comments for the associated post
    def get_num_comments(self, obj):
        return Comment.objects.filter(post=obj.post).count()


# Serializer for the like model
class LikeSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user',)


# REST API
# Serializer for comment model for all users
class CommentAllUsersSerializer(CommentSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


# Serializer for like model for all users
class LikeAllUsersSerializer(LikeSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Like
        fields = '__all__'

# I wrote this code
