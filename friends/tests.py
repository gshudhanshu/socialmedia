from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import *
from .serializers import *
from .factories import *


# I wrote this code
class FriendModelTest(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_friend_accept(self):
        # Create a friend request
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)
        # Check if the friend request is not accepted
        self.assertFalse(friend_request.accepted)
        friend_request.accept()
        # Check if the friend request is accepted
        self.assertTrue(friend_request.accepted)

    def test_friend_decline(self):
        # Create a friend request
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)
        # Check if the friend request is not accepted
        self.assertFalse(friend_request.accepted)
        # Decline the friend request
        friend_request.decline()
        # Check if the friend request is not accepted
        self.assertIsNone(Friend.objects.filter(id=friend_request.id).first())


class FriendAPITest(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_list_friends(self):
        # Create a friend request
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=True)

        # Get the URL for the list of friends
        url = reverse('api-friend-list', args=[self.user1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user1.id)
        self.assertEqual(response.data[0]['friend'], self.user2.id)

    def test_list_friend_requests_received(self):
        # Create a friend request
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        # Get the URL for the list of friends
        url = reverse('api-friend-requests-received', args=[self.user2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user1.id)
        self.assertEqual(response.data[0]['friend'], self.user2.id)

    def test_list_friend_requests_sent(self):
        # Create a friend request
        friend_request = FriendFactory(user=self.user1, friend=self.user2, accepted=False)

        #  Get the URL for the list of friends
        url = reverse('api-friend-requests-sent', args=[self.user1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['friend'], self.user2.id)
        self.assertEqual(response.data[0]['user'], self.user1.id)

# end of code I wrote
