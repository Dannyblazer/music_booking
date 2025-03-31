from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.tests.factories import UserFactory, ArtistProfileFactory

class PermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist_user = UserFactory(role='artist')
        self.booker_user = UserFactory(role='booker')

    def test_booker_cannot_update_artist_profile(self):
        artist = ArtistProfileFactory(user=self.artist_user)
        self.client.force_authenticate(user=self.booker_user)
        response = self.client.put(f'/api/artists/{artist.id}/', {'stage_name': 'New Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/artists/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)