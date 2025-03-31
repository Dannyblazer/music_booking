from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.cache import cache
from account.tests.factories import UserFactory, ArtistProfileFactory

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist_user = UserFactory(role='artist')
        self.booker_user = UserFactory(role='booker')
        self.client.force_authenticate(user=self.artist_user)

    def test_user_register(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'role': 'booker',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_artist_list_cached(self):
        ArtistProfileFactory.create_batch(3)
        response = self.client.get('/api/artists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Paginated response
        self.assertEqual(len(response.data['results']), 3)

        cache_key = "artists_list_all"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data['results']), 3)