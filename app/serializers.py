import base64

from rest_framework import serializers

from .encryption import decrypt_data
from .models import AppUser, Message, MessageEncrypted


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class SendMessageSerializer(serializers.Serializer):
    user_from = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    user_to = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    content = serializers.CharField()

    # This field is not stored. Combine the content with the key to encrypt
    # User's responsibility to remember their encryption key.
    key = serializers.CharField(required=False)


class DecryptedMessageSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    salt = serializers.IntegerField()
    user_from = serializers.UUIDField()
    user_to = serializers.UUIDField()
    content = serializers.CharField()


class EncryptedMessageSerializer(serializers.ModelSerializer):
    # in case user requests non-decrypted data back, provide as all strings (as per model)
    class Meta:
        model = MessageEncrypted
        fields = '__all__'


class ListMessageSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        if 'encrypted_serializer' in kwargs:
            self.encrypted = kwargs.pop('encrypted_serializer')
        super().__init__(*args, **kwargs)

    id = serializers.UUIDField()
    encrypted = EncryptedMessageSerializer()  # default but may be overridden
