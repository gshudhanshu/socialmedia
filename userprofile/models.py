from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    # first_name = models.CharField(max_length=30, blank=True, null=True)
    # last_name = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile', default='profile/default.jpg',
                                      blank=True, null=True)
    status_message = models.TextField(max_length=1000, blank=True, null=True)
    status_updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Use a signal to create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,
                                   date_of_birth=instance.date_of_birth,
                                   profile_image=instance.profile_image)


# Use a signal to save the UserProfile when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'date_of_birth') and hasattr(instance, 'profile_image'):
        instance.userprofile.date_of_birth = instance.date_of_birth
        instance.userprofile.profile_image = instance.profile_image
        instance.userprofile.save()
