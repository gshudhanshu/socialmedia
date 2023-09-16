from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .serializers import *
from .factories import *
from authentication.factories import UserFactory


# I wrote this code
class ChatRoomAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('api-chat-view')
        self.user = UserFactory()
        self.chatroom_data = ChatRoomFactory()

    # test for creating new chatroom
    def test_create_chatroom(self):
        chatroom_data = ChatRoomSerializer(self.chatroom_data).data
        response = self.client.post(self.url,
                                    {"name": chatroom_data['name']},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 2)
        self.assertEqual(response.data['name'], chatroom_data['name'])

    # test for listing chatrooms
    def test_list_chatrooms(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChatRoom.objects.count(), 1)


class ChatMessageAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('api-chat-room-view', args=['test'])
        self.user = UserFactory()
        self.chatroom_data = ChatRoomFactory()
        self.chatmessage_data = ChatMessageFactory(room_name=self.chatroom_data, user=self.user)

    # test for creating new chat message
    def test_create_chatmessage(self):
        chatmessage_data = ChatMessageSerializer(self.chatmessage_data).data  # Serialize the ChatMessage instance
        response = self.client.post(self.url, chatmessage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatMessage.objects.count(), 2)  # Check if a new chat message was created
        self.assertEqual(response.data['message'], chatmessage_data['message'])
        self.assertEqual(response.data['user'], chatmessage_data['user'])

    # test for listing chat messages
    def test_list_chatmessages(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(response.data[0]['message'], self.chatmessage_data.message)
        self.assertEqual(response.data[0]['user'], self.chatmessage_data.user.id)

# end of code I wrote
