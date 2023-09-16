from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import *
from .serializers import *
from .factories import *


class FriendModelTest(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_friend_accept(self):
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        self.assertFalse(friend_request.accepted)
        friend_request.accept()
        self.assertTrue(friend_request.accepted)

    def test_friend_decline(self):
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        self.assertFalse(friend_request.accepted)
        friend_request.decline()
        self.assertIsNone(Friend.objects.filter(id=friend_request.id).first())


class FriendAPITest(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_list_friends(self):
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=True)

        url = reverse('api-friend-list', args=[self.user1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_friend_requests_received(self):
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        url = reverse('api-friend-requests-received', args=[self.user2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_friend_requests_sent(self):
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        url = reverse('api-friend-requests-sent', args=[self.user1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
