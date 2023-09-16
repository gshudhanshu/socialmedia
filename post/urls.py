from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.ListPosts.as_view(), name='home'),
    path('post/create', views.CreatePostAPI.as_view(), name='createpost'),
    path('comment/create', views.CreateCommentAPI.as_view(), name='createcomment'),
    path('comments/<int:post_id>', views.ListCommentsAPI.as_view(), name='listcomments'),
    path('like/<int:post_id>', views.LikePostAPI.as_view(), name='like'),

    # REST API URLS
    path('api/user-posts/<int:user_id>', api.ListUserPosts.as_view(), name='api-user-posts'),
    path('api/posts/<int:post_id>', api.ViewPost.as_view(), name='api-post'),
    path('api/posts/<int:post_id>/comments', api.ListPostComments.as_view(), name='api-post-comments'),
    path('api/posts/<int:post_id>/like', api.LikePost.as_view(), name='api-like-post'),
]
