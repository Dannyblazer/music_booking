from django.test import TestCase
from account.models import User, ArtistProfile
from account.tests.factories import UserFactory, ArtistProfileFactory

class ModelTests(TestCase):
    def test_user_creation(self):
        # Explicitly set the sequence to start at 0 for this test
        user = UserFactory(role='artist', email='user0@example.com')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, "user0@example.com")
        self.assertEqual(user.role, 'artist')

    def test_artist_profile_creation(self):
        artist = ArtistProfileFactory()
        self.assertEqual(artist.stage_name, "Artist0")
        self.assertTrue(artist.is_available)
        self.assertEqual(artist.user.role, 'artist')