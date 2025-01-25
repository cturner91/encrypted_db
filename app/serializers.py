import base64

from rest_framework import serializers

from .encryption import decrypt_data
from .models import AppUser, Message


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


class ListMessageSerializer(serializers.Serializer):
    user_from = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    user_to = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    # This field is not stored. User's responsibility to remember their encryption key.
    key = serializers.CharField()
