from django.contrib.auth.models import User
from rest_framework import serializers
from userprofile.models import UserProfile


# I wrote this code
# Serializer for the user profile model
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# REST API Serializer
# Serializer for the user profile model API
class UserProfileAPISerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password',
                  'userprofile']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     # Remove 'date_of_birth' and 'profile_image' from 'validated_data' for 'User' creation
    #     date_of_birth = validated_data.pop('date_of_birth', None)
    #     profile_image = validated_data.pop('profile_image', None)
    #
    #     # Create a new user
    #     user = User.objects.create_user(**validated_data)
    #
    #     # Create or update the user profile
    #     if date_of_birth or profile_image:
    #         user_profile, created = UserProfile.objects.get_or_create(user_id=user.id)
    #         if date_of_birth:
    #             user_profile.date_of_birth = date_of_birth
    #         if profile_image:
    #             user_profile.profile_image = profile_image
    #         user_profile.save()
    #
    #     return user

# end of code I wrote
