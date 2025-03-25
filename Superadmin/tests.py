from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from utilisateurs.models import User
from .models import Publication, Transaction

class SuperadminTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='password',
            role='admin'
        )
        self.client.login(username='admin', password='password')

    def test_user_management(self):
        response = self.client.get(reverse('user-management'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publication_management(self):
        response = self.client.post(reverse('publication-management'), {
            'title': 'Test Publication',
            'content': 'This is a test publication.',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transaction_management(self):
        response = self.client.get(reverse('transaction-management'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
