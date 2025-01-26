import os
from uuid import uuid4

from django.db import models

from .encryption import decrypt_data, encrypt_data


class EncryptedMixin(models.Model):
    '''This class encrypts all fields except ID

    Use as a OneToOne relationship on another model, with the fields requiring encryption on this
    model and the fields not requiring encryption on the sibling model

    As everything is base64 encoded, all fields on subclass **must** be strings. They can be 
    converted into their representative types using serializers.
    '''
    id = models.UUIDField(primary_key=True, default=uuid4)
    salt = models.CharField(max_length=32)  # 16-byte digit is too big for even BigIntegerField

    class Meta:
        abstract = True

    def _concrete_field_names(self) -> list[str]:
        return [field.name for field in self._meta.fields if not field.is_relation]

    def encrypt(self, key: str = None):
        if key is None:
            return self  # assume already encrypted

        # generate random salt
        self.salt = int.from_bytes(os.urandom(16), byteorder='big')

        for field in self._concrete_field_names():
            if field in ('id', 'salt'):
                continue

            value = str(getattr(self, field))
            encrypted = encrypt_data(key, int(self.salt), value)
            setattr(self, field, encrypted)

        return self

    def decrypt(self, key: str = None):
        if key is None:
            return self  # assume already decrypted

        for field in self._concrete_field_names():
            if field in ('id', 'salt'):
                continue

            value = str(getattr(self, field))
            decrypted = decrypt_data(key, int(self.salt), value)  # let errors raise
            setattr(self, field, decrypted)

        return self


class AppUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=20)  # something I can use to recognise users
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class MessageEncrypted(EncryptedMixin):
    # All fields under an EncryptedMixin must be TextFields
    created_at = models.TextField()
    user_from = models.TextField()
    user_to = models.TextField()
    content = models.TextField()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    encrypted = models.OneToOneField(MessageEncrypted, on_delete=models.CASCADE)
