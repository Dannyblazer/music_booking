from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def update_artist_availability(sender, instance, created, **kwargs):
    if not created and instance.status == 'confirmed':
        artist = instance.artist
        artist.is_available = False
        artist.save()
    elif instance.status == 'canceled':
        artist = instance.artist
        artist.is_available = True
        artist.save()