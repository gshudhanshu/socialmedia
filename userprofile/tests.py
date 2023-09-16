from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import *


class UserProfileViewTestCase(APITestCase):
    def setUp(self):
        # Create test users with profiles
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_list_profiles(self):
        url = reverse('api-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], self.user1.username)
        self.assertEqual(response.data[1]['username'], self.user2.username)

    def test_view_profile(self):
        # Create a user profile using the factory
        user_profile = UserFactory()

        url = reverse('api-profile', kwargs={'user_id': user_profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user_profile.username)
        self.assertEqual(response.data['email'], user_profile.email)
        self.assertEqual(response.data['first_name'], user_profile.first_name)
        self.assertEqual(response.data['last_name'], user_profile.last_name)

    def test_view_profile_not_found(self):
        non_existent_user_id = 999999
        url = reverse('api-profile', kwargs={'user_id': non_existent_user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
