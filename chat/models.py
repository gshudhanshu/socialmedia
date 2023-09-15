from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# Create class for chat room
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    online = models.ManyToManyField(User, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return self.name + ' (' + str(self.get_online_count()) + ')'


# Create class for chat message
class ChatMessage(models.Model):
    room_name = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.message
