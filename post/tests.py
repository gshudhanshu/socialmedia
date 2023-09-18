from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import *


# I wrote this code
# Test cases for Post API
class PostViewTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        # Create test data, such as posts, comments, and likes
        self.post = Post.objects.create(user=self.user1, title='Test Post', content='This is a test post')
        self.comment = Comment.objects.create(user=self.user1, post=self.post, content='Test Comment')
        self.like = Like.objects.create(user=self.user1, post=self.post)

    def test_view_post(self):
        url = reverse('api-post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)
        self.assertEqual(response.data['content'], self.post.content)

    def test_list_post_comments(self):
        url = reverse('api-post-comments', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.comment.content)
        self.assertEqual(response.data[0]['user'], self.comment.user.id)

    def test_like_post(self):
        url = reverse('api-like-post', args=[self.post.id])
        data = {'user': self.user1.id, 'post': self.post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# I wrote this code
