from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from event.models import Event, Booking
from event.serializers import EventSerializer, BookingSerializer
from account.tests.factories import UserFactory, ArtistProfileFactory, EventFactory, BookingFactory
from event.views import send_booking_confirmation_email

class ModelTests(TestCase):
    def test_event_creation(self):
        event = EventFactory(title='Event0')
        self.assertEqual(event.title, "Event0")
        self.assertEqual(event.status, 'pending')
        self.assertTrue(hasattr(event, 'created_by'))

    def test_booking_creation(self):
        booking = BookingFactory()
        self.assertEqual(booking.total_amount, 150.00)
        self.assertEqual(booking.status, 'pending')
        self.assertTrue(hasattr(booking, 'event'))

class SerializerTests(APITestCase):
    def test_event_serializer(self):
        event = EventFactory()
        serializer = EventSerializer(event)
        data = serializer.data
        self.assertEqual(data['title'], event.title)
        self.assertIn('created_by', data)
        self.assertEqual(data['status'], 'pending')

    def test_booking_serializer(self):
        booking = BookingFactory()
        serializer = BookingSerializer(booking)
        data = serializer.data
        self.assertEqual(float(data['total_amount']), 150.00)
        self.assertIn('event', data)
        self.assertIn('artist', data)

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.booker_user = UserFactory(role='booker')
        self.artist_user = UserFactory(role='artist')
        self.client.force_authenticate(user=self.booker_user)

    def test_create_event_as_booker(self):
        data = {
            'title': 'New Event',
            'description': 'Test event',
            'date_time': '2025-04-01T12:00:00Z',
            'location': 'Test Venue'
        }
        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Event')
        self.assertEqual(response.data['created_by']['id'], str(self.booker_user.id))

    def test_create_booking_triggers_celery(self):
        event = EventFactory(created_by=self.booker_user)
        artist = ArtistProfileFactory()
        data = {
            'event_id': str(event.id),
            'artist_id': str(artist.id),
            'total_amount': 200.00
        }
        # Ensure Celery tasks run synchronously
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True):
            response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')

    def test_confirm_booking_as_artist(self):
        booking = BookingFactory(artist__user=self.artist_user, booker=self.booker_user)
        self.client.force_authenticate(user=self.artist_user)
        response = self.client.patch(f'/api/bookings/{booking.id}/confirm/', {'status': 'confirmed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')