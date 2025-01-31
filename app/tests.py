from django.test import Client, TestCase

from .encryption import decrypt_data, encrypt_data
from .models import AppUser, Message


class EncryptionTests(TestCase):

    def test__encrypted_then_decrypted_returns_same_result(self):
        # I really have no way to validate that the encryption has been done correctly, so I'm 
        # simply going to verify that the encrypted value is not equal to the unencrypted value,
        # and that the decrypted value equals the original value
        test_string = 'Please encrypt me'
        key = 'ABCDEFG'
        salt = 123

        encrypted = encrypt_data(key, salt, test_string)
        self.assertNotEqual(test_string, encrypted)
        self.assertIsInstance(encrypted, str)

        decrypted = decrypt_data(key, salt, encrypted)
        self.assertEqual(decrypted, test_string)
        self.assertIsInstance(decrypted, str)
    
    def test__encrypted_different_keys_produces_different_values(self):
        test_string = 'Please encrypt me'
        key1 = 'ABCDEFG'
        key2 = '1234567'
        salt = 123456

        encrypted1 = encrypt_data(key1, salt, test_string)
        encrypted2 = encrypt_data(key2, salt, test_string)

        self.assertNotEqual(encrypted1, encrypted2)

    def test__decrypt_with_bad_key_fails(self):
        test_string = 'Please encrypt me'
        salt = 1234567890

        encrypted = encrypt_data('ABCDEFG', salt, test_string)
        self.assertNotEqual(test_string, encrypted)

        with self.assertRaises(Exception):
            decrypt_data('1234567', salt, encrypted)

    def test__decrypt_with_bad_salt_fails(self):
        test_string = 'Please encrypt me'
        key = 'ABCDEFG'

        encrypted = encrypt_data(key, 123, test_string)
        self.assertNotEqual(test_string, encrypted)

        with self.assertRaises(Exception):
            decrypt_data(key, 124, encrypted)


class AppUsersApiTests(TestCase):

    def setUp(self):
        self.client = Client()

    # create is the only feature I really need for the README so don't bother testing update/delete
    def test__create(self):
        self.assertEqual(AppUser.objects.count(), 0)
        self.client.post('/api/app-users/', data={'name': 'User1'})
        self.assertEqual(AppUser.objects.count(), 1)


class SendMessageApiTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/api/send-message/'
        self.user1 = AppUser.objects.create(name='User1')
        self.user2 = AppUser.objects.create(name='User2')

        self.default_payload = {
            'user_from': self.user1.id, 
            'user_to': self.user2.id, 
            'content': 'This is some text',
        }

    def test__create_unencrypted(self):        
        self.assertEqual(Message.objects.count(), 0)
        self.client.post(self.url, data=self.default_payload)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first()
        self.assertEqual(message.encrypted.content, 'This is some text')

    def test__create_encrypted(self):        
        self.assertEqual(Message.objects.count(), 0)
        self.client.post(self.url, data={
            **self.default_payload,
            'key': 'ABCD',
        })
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first()
        self.assertNotEqual(message.encrypted.content, 'This is some text')


class ViewMessageApiTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/api/view-messages/'
        self.user1 = AppUser.objects.create(name='User1')
        self.user2 = AppUser.objects.create(name='User2')

    def _generate_message(
        self, user_from: AppUser, user_to: AppUser, message: str, key: str = ''
    ):
        # again - I don't know how to encrypt/decrypt the data by hand to verify against, so let's 
        # use my previously-tested endpoint
        payload = {
            'user_from': user_from.id,
            'user_to': user_to.id,
            'content': message,
        }
        if key:
            payload['key'] = key

        self.client.post('/api/send-message/', data=payload)

    def test__view_unencrypted_without_key(self):
        self._generate_message(self.user1, self.user2, 'UN-encrypted')

        response = self.client.get(self.url)
        self.assertEqual(response.json()[0]['encrypted']['content'], 'UN-encrypted')

    def test__view_unencrypted_with_key(self):
        self._generate_message(self.user1, self.user2, 'UN-encrypted')

        response = self.client.get(f'{self.url}?key=abc')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], 'Could not be decrypted with that key.')

    def test__view_encrypted_without_key(self):
        self._generate_message(self.user1, self.user2, 'EN-crypted', key='abc')

        response = self.client.get(self.url)
        self.assertNotEqual(response.json()[0]['encrypted']['content'], 'EN-crypted')
        self.assertEqual(response.json()[0]['encrypted']['content'][-1], '=')

    def test__view_encrypted_with_key(self):        
        self._generate_message(self.user1, self.user2, 'EN-crypted', key='abc')

        response = self.client.get(f'{self.url}?key=abc')
        self.assertEqual(response.json()[0]['encrypted']['content'], 'EN-crypted')

    def test__multiple_messages_encrypted(self):
        for i in range(10):
            self._generate_message(self.user1, self.user2, f'This is message #{i}', key='12345')
        
        response = self.client.get(f'{self.url}?key=12345')
        data = response.json()
        self.assertEqual(len(data), 10)
        for i in range(len(data)):
            # 9-1 because messages are in reverse order (most recent first)
            self.assertEqual(data[i]['encrypted']['content'], f'This is message #{9-i}')
