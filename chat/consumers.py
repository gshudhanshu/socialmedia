import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, ChatMessage


#  I have taken the reference from
#  https://testdriven.io/blog/django-channels/ tutorial
# and modified it to suit my needs

# I wrote this code
# Chat consumer to handle websocket connections
class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    # connect to the websocket
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = ChatRoom.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'

        # connection is accepted
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # send newly joined user list to the room
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        # send the chat history to the newly joined user
        # Last 50 messages are sent
        history = ChatMessage.objects.filter(room_name=self.room).order_by('-created_at')[:50]
        history = reversed(history)
        self.send(json.dumps({
            'type': 'chat_history',
            'messages': [{
                'user': message.user.username,
                'message': message.message,
            } for message in history],
        }))

        if self.user.is_authenticated:
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)

    # disconnect from the websocket
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # delete the user inbox
            async_to_sync(self.channel_layer.group_discard)(
                self.user_inbox,
                self.channel_name,
            )

            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )

            self.room.online.remove(self.user)

    # receive message from the websocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )

        # save the message to the database
        ChatMessage.objects.create(user=self.user, room_name=self.room, message=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

# end of code I wrote
