import random
from datetime import datetime
from operator import attrgetter

from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AppUser, Message, MessageEncrypted
from .serializers import AppUserSerializer, SendMessageSerializer, ListMessageSerializer, EncryptedMessageSerializer, DecryptedMessageSerializer


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
            encrypted_serializer = EncryptedMessageSerializer
        else:
            for message in queryset:
                try:
                    message.encrypted.decrypt(key)
                except:
                    raise ValidationError('Could not be decrypted with that key.')

            encrypted_serializer = DecryptedMessageSerializer

        # if still encrypted, this is nonsensical -> which is what we want
        # Do not use queryset.order_by -> it re-encrypts data (must not be an in-place operation)
        queryset = sorted(queryset, key=lambda x: x.encrypted.created_at, reverse=True)

        serializer = ListMessageSerializer(
            queryset, many=True, encrypted_serializer=encrypted_serializer()
        )
        return Response(serializer.data, status=200)
