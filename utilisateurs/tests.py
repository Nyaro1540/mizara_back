from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, ProfileCollecteur

class ProfileCollecteurTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            nom_complet='Test User',
            prenom='Test',
            numero_telephone='0123456789',
            email='test@example.com',
            password='testpassword',
            lieu_habitation='Test Location'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_profile_collecteur(self):
        response = self.client.post('/api/profile-collecteur/', {
            'nif': '123456789',
            'stat': '12345678',
            'cin': '123456789'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.role, 'collecteur')

    def test_create_profile_collecteur_missing_fields(self):
        response = self.client.post('/api/profile-collecteur/', {
            'nif': '',
            'stat': '',
            'cin': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("NIF, STAT et CIN sont requis.", str(response.data))
