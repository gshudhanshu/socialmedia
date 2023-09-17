from random import sample
from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, OuterRef, Exists
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from django.views.generic import ListView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from friends.models import Friend
from post.models import Post, Comment, Like
from . import serializers


# I wrote this code
# View for List of Posts, Friend suggestions
class ListPosts(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home/posts.html'
    context_object_name = 'posts'

    # Get friend suggestions
    def get_friend_suggestions(self, count=10):
        all_users = User.objects.exclude(id=self.request.user.id)
        already_sent_users = Friend.objects.filter(user=self.request.user,
                                                   friend__in=all_users.values('id')).values_list('friend_id',
                                                                                                  flat=True)
        already_received_users = Friend.objects.filter(friend=self.request.user,
                                                       user__in=all_users.values('id')).values_list('user_id',
                                                                                                    flat=True)
        # Combine the two lists and exclude them from the all_users queryset
        excluded_users = set(already_sent_users) | set(already_received_users)
        all_users = all_users.exclude(id__in=excluded_users)

        total_users = all_users.count()
        if total_users < count:
            count = total_users
        # Get a random sample of users

        random_users = sample(list(all_users), count)
        return random_users

    # Get all posts with num_likes, num_comments, user_liked
    def get_queryset(self):
        user = self.request.user
        user_has_liked = Like.objects.filter(post=OuterRef('pk'), user=user)
        queryset = Post.objects.annotate(
            num_likes=Count('like', distinct=True),
            num_comments=Count('comment', distinct=True),
            user_liked=Exists(user_has_liked),
        ).order_by('-created_at')
        # Fetch comments and order them by creation date (desc)
        comment_prefetch = Prefetch('comment_set',
                                    queryset=Comment.objects.order_by('-created_at'))
        queryset = queryset.select_related('user__userprofile')
        queryset = queryset.prefetch_related(comment_prefetch)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['friend_suggestions'] = self.get_friend_suggestions()
        return context


# Create a post
class CreatePost(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = Post.objects.create(user=user, title=title, content=content, image=image)
        return HttpResponseRedirect(reverse('home'))


# Create a post
class CreatePostAPI(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # get the authenticated user
        global user
        user_id = self.request.data.get('user')
        if user_id:
            # if a user ID is provided, try to get the user or return None
            user = get_object_or_404(User, id=user_id)
        user = user or self.request.user
        serializer.save(user=user)


# Create new comment API
class CreateCommentAPI(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Get the authenticated user
        user = self.request.user

        # Get the post id from the URL
        post_id = request.data.get('post')
        post = get_object_or_404(Post, id=post_id)

        # Check if the user is authenticated
        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user'] = user
            serializer.validated_data['post'] = post
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User must be authenticated to create a comment"},
                            status=status.HTTP_403_FORBIDDEN)


# Get list of comments for a post
class ListCommentsAPI(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset


# Like or unlike a post
class LikePostAPI(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Get the authenticated user
        user = self.request.user

        # Get the post id from the URL
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        # Check if the user is authenticated
        if user.is_authenticated:
            # Check if the user has already liked the post
            if Like.objects.filter(user=user, post=post).exists():
                # If so, unlike the post
                Like.objects.filter(user=user, post=post).delete()
                num_likes = Like.objects.filter(post=post).count()
                return Response({'post': post_id, "message": "Post unliked",
                                 'liked': False, "num_likes": num_likes, },
                                status=status.HTTP_200_OK)
            else:
                # If not, like the post
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.validated_data['user'] = user
                serializer.validated_data['post'] = post
                self.perform_create(serializer)

                num_likes = Like.objects.filter(post=post).count()
                return Response({'post': post_id, "message": "Post liked",
                                 'liked': True, "num_likes": num_likes},
                                status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User must be authenticated to like a post"},
                            status=status.HTTP_403_FORBIDDEN)

# end of code I wrote
