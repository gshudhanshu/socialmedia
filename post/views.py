from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from django.views.generic import ListView

from post.models import Post, Comment, Like
from . import serializers


# Create your views here.

class Index(ListView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = serializers.PostSerializer
    permission_classes = (AllowAny,)
    template_name = 'home/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context


class CreatePostAPI(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = (AllowAny,)


class CreateCommentAPI(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)


class ListCommentsAPI(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset
