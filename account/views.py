from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .models import ArtistProfile
from .serializers import ArtistProfileSerializer, UserSerializer
from .permissions import IsArtist

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistProfileViewSet(viewsets.ModelViewSet):
    queryset = ArtistProfile.objects.select_related('user').all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsArtist()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        cache_key = f"artists_list_{request.query_params.get('genre', 'all')}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # Apply genre filter if provided
        queryset = self.get_queryset()
        if 'genre' in request.query_params:
            queryset = queryset.filter(genre=request.query_params['genre'])

        # Ensure pagination is applied
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        cache.set(cache_key, response.data, timeout=60*15)  # Cache the paginated response
        return response