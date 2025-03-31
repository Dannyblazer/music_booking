from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import ArtistProfile
from .serializers import ArtistProfileSerializer, UserSerializer
from .permissions import IsArtist


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if credentials are provided
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if user is active
            if not user.is_active:
                return Response(
                    {'error': 'This account is inactive'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Prepare response data
            serializer = UserSerializer(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }

            # Cache the user data (optional)
            cache_key = f"user_data_{user.id}"
            cache.set(cache_key, response_data, timeout=60*15)  # Cache for 15 minutes

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        

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

    def perform_create(self, serializer):
        # Set the user to the authenticated user
        serializer.save(user=self.request.user)

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
        cache.set(cache_key, response.data, timeout=60*15)
        return response