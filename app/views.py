import base64 

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .encryption import encrypt_data, decrypt_data
from .models import AppUser, Message
from .serializers import AppUserSerializer, MessageSerializer, SendMessageSerializer


class AppUserListView(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = SendMessageSerializer

    def perform_create(self, serializer):
        key = serializer.validated_data.get('encryption_key', '')
        content = serializer.validated_data['content']

        # if no key, leave content unencrypted
        if key:
            content = encrypt_data(key, content)
        
        message = Message.objects.create(
            user_from=serializer.validated_data['user_from'],
            user_to=serializer.validated_data['user_to'],
            content=content,
        )
        return message


class ListMessageView(APIView):
    
    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')
        queryset = Message.objects.all()

        if key:
            for message in queryset:
                try:
                    message.content = decrypt_data(key, message.content)
                except:
                    message.content = 'Could not be decrypted with that key.'

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
