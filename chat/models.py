from django.contrib.auth.models import User
from django.db import models


#  I have taken the reference from
#  https://testdriven.io/blog/django-channels/ tutorial
# and modified it to suit my needs

# I wrote this code
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    online = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # get the number of users online
    def get_online_count(self):
        return self.online.count()

    # add a user to the online list
    def join(self, user):
        self.online.add(user)
        self.save()

    # remove a user from the online list
    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return self.name + ' (' + str(self.get_online_count()) + ')'


class ChatMessage(models.Model):
    room_name = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.message

# end of code I wrote
