from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    ROLE_CHOICES = (
        ('artist', 'Artist'),
        ('booker', 'Booker'),
        ('admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['role']),
        ]

class ArtistProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    stage_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=50)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    profile_picture = models.ImageField(upload_to='artist_pics/', blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['genre', 'is_available']),
        ]