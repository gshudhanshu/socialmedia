from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse


# I wrote this code
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_request')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_request')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"

    # Accept the friend request and create a Friend relationship.
    def accept(self):
        if not self.accepted:
            self.accepted = True
            self.save()

    # Decline the friend request.
    def decline(self):
        if not self.accepted:
            self.delete()

    # Cancel the sent friend request.
    def cancel(self):
        if not self.accepted:
            self.delete()

    # Remove the friend.
    def remove(self):
        if self.accepted:
            self.delete()

# end of code I wrote
