from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('friends', views.ListFriends.as_view(), name='friends'),
    path('api/friends/add-friend', views.AddFriendAPI.as_view(), name='add-friend'),
    path('api/friends/accept-decline-cancel', views.AcceptOrDeclineCancelFriendAPI.as_view(),
         name='accept-decline-cancel'),
    # path('/friends/accept-friend', views.AcceptFriend.as_view(), name='accept-friend'),
    # path('/friends/decline-friend', views.DeclineFriend.as_view(), name='decline-friend'),
    # path('/friends/remove-friend', views.RemoveFriend.as_view(), name='remove-friend'),
]
