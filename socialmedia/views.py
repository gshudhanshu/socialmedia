# I wrote this code
# REST-API LINKS PAGE
from django.shortcuts import render
from django.views import View


class RestApiLinks(View):
    rest_apis = [
        {'title': 'List Chat rooms', 'url': '/api/chat'},
        {'title': 'Chat room: 1 details', 'url': '/api/chat/1'},
        {'title': 'Get the friend list of user_id: 1', 'url': '/api/friend-list/1'},
        {'title': 'Get the friend requests list received by user_id: 1', 'url': '/api/friend-requests-received/1'},
        {'title': 'Get the friend requests list sent by user_id: 1', 'url': '/api/friend-requests-sent/1'},
        {'title': 'List user posts by user_id: 1', 'url': '/api/user-posts/1'},
        {'title': 'List post comments with post_id: 1', 'url': '/api/posts/1/comments'},
        {'title': 'List post likes with post_id: 1', 'url': '/api/posts/1/like'},
        {'title': 'List user profiles', 'url': '/api/profiles'},
        {'title': 'Get user profile with user_id: 1', 'url': '/api/profiles/1'},

    ]

    def get(self, request):
        return render(request, 'rest_apis/rest-apis.html', {'rest_apis': self.rest_apis})

# end of code I wrote
