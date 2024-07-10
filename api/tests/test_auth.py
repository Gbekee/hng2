from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'

    def test_register_user_successfully(self):
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "password": "strongpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data['data'])

    def test_login_user_successfully(self):
        User.objects.create_user(firstName='Jane', lastName='Doe', email='jane.doe@example.com', phone='0987654321', password='strongpassword')
        data = {
            "email": "jane.doe@example.com",
            "password": "strongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])

    def test_register_user_missing_fields(self):
        data = {
            "firstName": "John",
            "lastName": "Doe"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate_email(self):
        User.objects.create_user(firstName='John', lastName='Doe', email='john.doe@example.com', phone='1234567890', password='strongpassword')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "0987654321",
            "password": "anotherpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_generation(self):
        user = User.objects.create_user(firstName='Token', lastName='User', email='token.user@example.com', phone='1234567890', password='strongpassword')
        refresh = RefreshToken.for_user(user)
        self.assertEqual(refresh.payload['user_id'], user.id)
