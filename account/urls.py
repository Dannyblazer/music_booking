from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistProfileViewSet, UserRegisterView, UserLoginView

router = DefaultRouter()
router.register(r'artists', ArtistProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
]