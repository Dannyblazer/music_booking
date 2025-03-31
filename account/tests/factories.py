import factory
from django.utils import timezone
from account.models import User, ArtistProfile
from event.models import Event, Booking

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    role = 'booker'

class ArtistProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArtistProfile

    user = factory.SubFactory(UserFactory, role='artist')
    stage_name = factory.Sequence(lambda n: f"Artist{n}")
    bio = "A talented artist"
    genre = "Rock"
    rate_per_hour = 100.00

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Sequence(lambda n: f"Event{n}")
    description = "A great event"
    date_time = factory.LazyFunction(timezone.now)
    location = "Venue"
    created_by = factory.SubFactory(UserFactory)
    status = 'pending'

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    event = factory.SubFactory(EventFactory)
    artist = factory.SubFactory(ArtistProfileFactory)
    booker = factory.SubFactory(UserFactory)
    total_amount = 150.00
    status = 'pending'