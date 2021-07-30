from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='messages')
    date_time = models.DateTimeField(auto_now_add=True)
