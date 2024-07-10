from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Organisation

class OrganisationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(firstName='John', lastName='Doe', email='john.doe@example.com', phone='1234567890', password='strongpassword')
        self.user2 = User.objects.create_user(firstName='Jane', lastName='Doe', email='jane.doe@example.com', phone='0987654321', password='strongpassword')
        self.org1 = Organisation.objects.create(name="John's Organisation")
        self.org1.user.add(self.user1)
        self.org2 = Organisation.objects.create(name="Jane's Organisation")
        self.org2.user.add(self.user2)
        self.client.force_authenticate(user=self.user1)
        self.organisation_url = '/api/organisations/'

    def test_user_cannot_see_other_organisations(self):
        response = self.client.get(self.organisation_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['organisations']), 2)
        self.assertEqual(response.data['organisations'][0]['name'], "John's Organisation")

    def test_create_organisation(self):
        data = {
            "name": "New Organisation"
        }
        response = self.client.post(self.organisation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "New Organisation")
