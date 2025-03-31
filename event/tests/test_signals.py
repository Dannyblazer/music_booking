from django.test import TestCase
from account.tests.factories import BookingFactory, ArtistProfileFactory

class SignalTests(TestCase):
    def test_artist_availability_on_booking_confirmed(self):
        artist = ArtistProfileFactory(is_available=True)
        booking = BookingFactory(artist=artist, status='pending')
        self.assertTrue(artist.is_available)

        booking.status = 'confirmed'
        booking.save()
        artist.refresh_from_db()
        self.assertFalse(artist.is_available)

    def test_artist_availability_on_booking_canceled(self):
        artist = ArtistProfileFactory(is_available=False)
        booking = BookingFactory(artist=artist, status='confirmed')
        booking.status = 'canceled'
        booking.save()
        artist.refresh_from_db()
        self.assertTrue(artist.is_available)