from django.test import TestCase
from rest_framework.test import APIClient
from utilisateurs.models import User, ProfileCollecteur

class ProfileCollecteurTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            nom_complet='Test User',
            prenom='Test',
            numero_telephone='0123456789',
            email='test@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_profile_collecteur(self):
        response = self.client.post('/api/profile_collecteur/', {
            'nif': '123456789',
            'stat': '12345678',
            'cin': '123456789'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'collecteur')  # Verify that the user's role is set to collecteur

        self.assertEqual(self.user.role, 'collecteur')
        self.assertEqual(response.status_code, 201)
        self.assertIn('nif', response.data)
        self.assertIn('stat', response.data)
        self.assertIn('cin', response.data)
