from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, Case, When, Value, BooleanField
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from django.views.generic import ListView
from rest_framework.response import Response

from post.models import Post, Comment, Like
from . import serializers


# Create your views here.

class ListPosts(ListView):
    model = Post
    template_name = 'home/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Annotate the number of likes and comments for each post
        queryset = Post.objects.annotate(
            num_likes=Count('like', distinct=True),
            num_comments=Count('comment', distinct=True),
            user_liked=Case(
                When(like__user=self.request.user, then=True),
                default=False,
                output_field=BooleanField(),
            )
        )

        # Use Prefetch to fetch comments and order them by creation date (desc)
        comment_prefetch = Prefetch('comment_set', queryset=Comment.objects.order_by('-created_at'))
        # Use select_related to fetch user profiles
        queryset = queryset.select_related('user__userprofile')
        # Add the comment prefetch
        queryset = queryset.prefetch_related(comment_prefetch)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional debugging information to the context
        context['debug_info'] = {
            'request_user': self.request.user,
            'queryset_count': len(context['posts']),
        }

        return context


class CreatePostAPI(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Get the authenticated user making the request
        user = self.request.user

        # Set the user for the created post
        serializer.save(user=user)


class CreateCommentAPI(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Get the authenticated user making the request
        user = self.request.user

        # Get the post id from the URL
        post_id = request.data.get('post')
        post = get_object_or_404(Post, id=post_id)

        # Ensure the user is authenticated
        if user.is_authenticated:
            # Set the user and post in the serializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user'] = user
            serializer.validated_data['post'] = post
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User must be authenticated to create a comment"},
                            status=status.HTTP_403_FORBIDDEN)


class ListCommentsAPI(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset


class LikePostAPI(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Get the authenticated user making the request
        user = self.request.user

        # Get the post id from the URL
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        # Ensure the user is authenticated
        if user.is_authenticated:
            # Check if the user has already liked the post
            if Like.objects.filter(user=user, post=post).exists():
                # If so, unlike the post
                Like.objects.filter(user=user, post=post).delete()
                num_likes = Like.objects.filter(post=post).count()
                return Response({'post': post_id, "message": "Post unliked", 'liked': False, "num_likes": num_likes, },
                                status=status.HTTP_200_OK)
            else:
                # If not, like the post
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.validated_data['user'] = user
                serializer.validated_data['post'] = post
                self.perform_create(serializer)

                num_likes = Like.objects.filter(post=post).count()
                return Response({'post': post_id, "message": "Post liked", 'liked': True, "num_likes": num_likes},
                                status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User must be authenticated to like a post"},
                            status=status.HTTP_403_FORBIDDEN)
