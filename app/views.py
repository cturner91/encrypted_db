import base64 
import json
import random
from datetime import datetime

from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .encryption import encrypt_data, decrypt_data
from .models import AppUser, Message, MessageEncrypted
from .serializers import AppUserSerializer, MessageSerializer, SendMessageSerializer, EncryptedListMessageSerializer, DecryptedListMessageSerializer


class AppUserListView(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = SendMessageSerializer

    def post(self, request):
        message_enc = MessageEncrypted(
            user_from=request.data['user_from'],
            user_to=request.data['user_to'],
            content=request.data['content'],
            salt=random.randint(0, 1000),
            created_at=datetime.now().isoformat(),
        )
        if key := request.data.get('key'):
            message_enc.encrypt(key)  # modifies state in-place

        message = Message(encrypted=message_enc)

        with transaction.atomic():
            message_enc.save()
            message.save()

        return Response({'message': 'Message created'}, 201)


class ListMessageView(APIView):
    
    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')
        queryset = Message.objects.all().select_related('encrypted')

        if not key:
            serializer = EncryptedListMessageSerializer(queryset, many=True)        
        else:
            for message in queryset:
                try:
                    message.encrypted.decrypt(key)
                except:
                    raise ValidationError('Could not be decrypted with that key.')

            serializer = DecryptedListMessageSerializer(queryset, many=True)

        return Response(serializer.data, status=200)
