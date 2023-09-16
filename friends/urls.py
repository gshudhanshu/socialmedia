from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('friends', views.ListFriends.as_view(), name='friends'),
    path('search', views.SearchUsers.as_view(), name='search-users'),
    path('api/friends/add-friend', views.AddFriendAPI.as_view(), name='add-friend'),
    path('api/friends/accept-decline-cancel-remove', views.AcceptOrDeclineCancelRemoveFriendAPI.as_view(),
         name='accept-decline-cancel-remove'),

    #   REST API URLS
    
]
