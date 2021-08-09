from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Message(models.Model):
    text = models.CharField(max_length=200, default='')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='messages')
    date_time = models.DateTimeField(auto_now_add=True)
    group = models.CharField(max_length=200)
    image = models.ImageField(default='')


# a profile model created when the user registers
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    profile_picture = models.ImageField(default='default.png')
    is_online = models.BooleanField(default=False)


# a model for the chat group
class ChatGroup(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name='chat_groups')
    name = models.CharField(max_length=200)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
