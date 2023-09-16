from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import OuterRef, Count, Exists, Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers

from friends.models import Friend
from post.models import Like, Post, Comment
from .forms import CustomUserChangeForm
from .models import UserProfile


# Create your views here.


class ProfileView(ListView):
    template_name = 'profile/profile.html'
    context_object_name = 'friend_profile'

    def get_authenticated_user(self):
        #  get authenticated user profile
        user = self.request.user
        return user

    def get_queryset(self):
        # get details of authenticated user
        user_id = self.kwargs.get('user_id') or self.request.user.id

        queryset = User.objects.filter(id=user_id).select_related('userprofile').first()
        return queryset

    def get_user_posts(self):
        #     if user_id is provided in url, get posts of that user
        #     else get posts of authenticated user
        user_id = self.kwargs.get('user_id') or self.request.user.id

        user_posts = Post.objects.filter(user_id=user_id).annotate(
            num_likes=Count('like', distinct=True),
            num_comments=Count('comment', distinct=True),
            user_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)),
        ).select_related('user__userprofile')
        # Use Prefetch to fetch comments and order them by creation date (desc)
        comment_prefetch = Prefetch('comment_set', queryset=Comment.objects.order_by('-created_at'))
        # Add the comment prefetch
        user_posts = user_posts.prefetch_related(comment_prefetch)
        return user_posts

    def get_friends(self):
        user_id = self.kwargs.get('user_id') or self.request.user.id

        friends = Friend.objects.filter(user_id=user_id, accepted=True).select_related(
            'friend__userprofile')
        friends = friends | Friend.objects.filter(friend_id=user_id, accepted=True).select_related(
            'user__userprofile')
        return friends

    def get_relationship(self):
        # get relationship between authenticated user and user in url
        user_id = self.kwargs.get('user_id') or self.request.user.id

        query = Friend.objects.filter(user_id=user_id, friend_id=self.request.user.id).first()
        if query is None:
            query = Friend.objects.filter(user_id=self.request.user.id, friend_id=user_id).first()

        if user_id == self.request.user.id:
            relationship = 'self'
        elif query is None:
            relationship = 'none'
        elif query.accepted:
            relationship = 'friends'
        elif query.user_id == self.request.user.id:
            relationship = 'sent'
        else:
            relationship = 'received'
        return relationship, query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_user_posts()
        context['friends'] = self.get_friends()
        context['user'] = self.get_authenticated_user()
        context['relationship'] = self.get_relationship()
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile/edit-profile.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user-profile-detail')  # Redirect to the profile page upon successful update

    def get_object(self, queryset=None):
        # Return the user's profile, which includes date_of_birth and profile_image
        return User.objects.filter(id=self.request.user.id).select_related('userprofile').first()

    def get_form(self, form_class=None):
        # Get the form and set the initial values for date_of_birth and profile_image
        form = super().get_form(form_class)
        form.fields['date_of_birth'].initial = self.request.user.userprofile.date_of_birth
        form.fields['profile_image'].initial = self.request.user.userprofile.profile_image
        return form

    def form_valid(self, form):
        # You can add additional logic here if needed
        return super().form_valid(form)


class UpdateStatusAPI(UpdateAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        # get authenticated user profile
        user = self.request.user
        return UserProfile.objects.get(user=user)

    def update(self, request, *args, **kwargs):
        # update status of authenticated user
        instance = self.get_object()
        instance.status_message = request.data.get('status_message')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
