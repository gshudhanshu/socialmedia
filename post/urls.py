from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListPosts.as_view(), name='home'),
    path('api/post/create', views.CreatePostAPI.as_view(), name='createpost'),
    path('api/comment/create', views.CreateCommentAPI.as_view(), name='createcomment'),
    path('api/comments/<int:post_id>', views.ListCommentsAPI.as_view(), name='listcomments'),
    path('api/like/<int:post_id>', views.LikePostAPI.as_view(), name='like'),
    # path('api/likes/<int:post_id>', views.LikesAPI.as_view(), name='likes'),
]
