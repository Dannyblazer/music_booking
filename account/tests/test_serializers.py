from rest_framework.test import APITestCase
from account.serializers import UserSerializer, ArtistProfileSerializer
from account.tests.factories import ArtistProfileFactory

class SerializerTests(APITestCase):
    def test_user_serializer(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'role': 'booker',
            'password': 'testpass123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'test@example.com')

    def test_artist_profile_serializer(self):
        artist = ArtistProfileFactory()
        serializer = ArtistProfileSerializer(artist)
        data = serializer.data
        self.assertEqual(data['stage_name'], artist.stage_name)
        self.assertEqual(data['genre'], 'Rock')
        self.assertIn('user', data)