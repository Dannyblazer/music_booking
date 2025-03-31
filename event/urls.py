from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]