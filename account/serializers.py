from rest_framework import serializers
from .models import User, ArtistProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class ArtistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Read-only, set by the view

    class Meta:
        model = ArtistProfile
        fields = ['id', 'user', 'stage_name', 'bio', 'genre', 'rate_per_hour', 'profile_picture', 'is_available']