from django.contrib import admin
from django.urls import path, include
from . import views
from . import api

urlpatterns = [
    path('friends', views.ListFriends.as_view(), name='friends'),
    path('search', views.SearchUsers.as_view(), name='search-users'),
    path('friends/add-friend', views.AddFriendAPI.as_view(), name='add-friend'),
    path('friends/accept-decline-cancel-remove', views.AcceptOrDeclineCancelRemoveFriendAPI.as_view(),
         name='accept-decline-cancel-remove'),

    #   REST API URLS
    path('api/friend-list/<int:user_id>', api.ListFriends.as_view(), name='api-friend-list'),
    path('api/friend-requests-received/<int:user_id>', api.ListFriendRequestsReceived.as_view(),
         name='api-friend-requests-received'),
    path('api/friend-requests-sent/<int:user_id>', api.ListFriendRequestsSent.as_view(),
         name='api-friend-requests-sent')

]
