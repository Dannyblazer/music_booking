from rest_framework import serializers
from .models import Event, Booking, ArtistProfile
from account.serializers import UserSerializer, ArtistProfileSerializer

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    artist = ArtistProfileSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'created_by', 'artist', 'status']

class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    artist = ArtistProfileSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(queryset=ArtistProfile.objects.all(), source='artist', write_only=True)
    booker = UserSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'event', 'event_id', 'artist', 'artist_id', 'booker', 'total_amount', 'status', 'created_at', 'payment_id']