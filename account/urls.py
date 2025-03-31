from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistProfileViewSet, UserRegisterView

router = DefaultRouter()
router.register(r'artists', ArtistProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
]