from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('api/createpost', views.CreatePostAPI.as_view(), name='createpost'),
    path('api/createcomment/<int:post_id>', views.CreateCommentAPI.as_view(), name='createcomment'),
    path('api/listcomments/<int:post_id>', views.ListCommentsAPI.as_view(), name='listcomments'),
    # path('api/like/<int:post_id>', views.LikeAPI.as_view(), name='like'),
    # path('api/likes/<int:post_id>', views.LikesAPI.as_view(), name='likes'),
]
