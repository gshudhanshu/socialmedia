from django.db.models import Count, Exists, OuterRef
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response


# I wrote this code
# API to list all posts of a user
class ListUserPosts(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(user_id=user_id).annotate(
            num_likes=Count('like', distinct=True),
            num_comments=Count('comment', distinct=True),
            user_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)),
        ).select_related('user__userprofile')

    # create new post with num_likes, num_comments, user_liked
    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # Create the new post
            post = serializer.save(user=self.request.user)

            # Annotate the num_likes, num_comments, and user_liked fields
            annotated_post = Post.objects.filter(pk=post.pk).annotate(
                num_likes=Count('like', distinct=True),
                num_comments=Count('comment', distinct=True),
                user_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)),
            ).select_related('user__userprofile').first()

            # Serialize the annotated post with the extra fields
            response_serializer = PostSerializer(annotated_post)

            return Response(response_serializer.data)
        # If serializer is not valid, return the errors
        return Response(serializer.errors)


# API to view a post with num_likes, num_comments, user_liked
class ViewPost(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.filter(id=post_id).annotate(
            num_likes=Count('like', distinct=True),
            num_comments=Count('comment', distinct=True),
        ).select_related('user__userprofile')

        # Check if the user is authenticated
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(
                user_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)),
            )

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Get list of post comments with user profile
class ListPostComments(ListCreateAPIView):
    serializer_class = CommentAllUsersSerializer

    def get_queryset(self):
        user = self.request.user
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).select_related('user__userprofile')


#  Like or unlike a post
class ListLikePost(ListCreateAPIView):
    serializer_class = LikeAllUsersSerializer

    def get_queryset(self):
        user = self.request.user
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id).select_related('user__userprofile')

    def create(self, request, *args, **kwargs):
        user = self.request.data.get('user')
        post = self.request.data.get('post')
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({'post_id': post, "message": "Post unliked", 'liked': False}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'post_id': post, "message": "Post liked", 'liked': True}, status=status.HTTP_200_OK)

# end of code I wrote
