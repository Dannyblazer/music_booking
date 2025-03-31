import factory
from django.utils import timezone
from event.models import Event, Booking
from account.tests.factories import UserFactory, ArtistProfileFactory

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