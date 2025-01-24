import base64
from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.db import models

from .encryption import decrypt_data, encrypt_data


class AppUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=20)  # something I can use to recognise users
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user_from = models.ForeignKey(
        AppUser, 
        on_delete=models.DO_NOTHING,
        related_name='messages_sent',
    )
    user_to = models.ForeignKey(
        AppUser, 
        on_delete=models.DO_NOTHING,
        related_name='messages_received',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
