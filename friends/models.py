from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_request')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_request')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"

    # class Meta:
    #     unique_together = ('user', 'friend')

    def accept(self):
        """
        Accept the friend request and create a Friend relationship.
        """
        if not self.accepted:
            self.accepted = True
            self.save()

    def decline(self):
        """
        Decline the friend request.
        """
        if not self.accepted:
            self.delete()

    def cancel(self):
        """
        Cancel the sent friend request.
        """
        if not self.accepted:
            self.delete()
