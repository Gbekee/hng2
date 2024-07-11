from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'
        self.user1 = User.objects.create_user(firstName='John', lastName='Doe', email='john.doe@example.com', phone='1234567890', password='strongpassword')
        self.user2 = User.objects.create_user(firstName='Jane', lastName='Doe', email='jane.doe@example.com', phone='0987654321', password='strongpassword')
        self.org1 = Organisation.objects.create(name="John's Organisation")
        self.org1.user.add(self.user1)
        self.org2 = Organisation.objects.create(name="Jane's Organisation")
        self.org2.user.add(self.user2)
        self.organisation_url = '/api/organisations/'

    def test_register_user_successfully(self):
        data = {
            "firstName": "Alice",
            "lastName": "Smith",
            "email": "alice.smith@example.com",
            "phone": "5555555555",
            "password": "strongpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data['data'])

    def test_login_user_successfully(self):
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

    def test_user_cannot_see_other_organisations(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.organisation_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['organisations']), 2)
        self.assertEqual(response.data['organisations'][0]['name'], "John's Organisation")

    def test_create_organisation(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "New Organisation"
        }
        response = self.client.post(self.organisation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "New Organisation")
