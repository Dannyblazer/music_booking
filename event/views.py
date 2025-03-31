from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer
from account.permissions import IsBooker, IsArtist
from celery import shared_task

@shared_task
def send_booking_confirmation_email(booking_id):
    print(f"Sending confirmation email for booking {booking_id}")

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('created_by', 'artist__user').all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsBooker()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'date' in request.query_params:
            queryset = queryset.filter(date_time__date=request.query_params['date'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
        

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('event__created_by', 'artist__user', 'booker').all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsBooker()]
        if self.action == 'confirm':
            return [IsArtist()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(booker=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_booking_confirmation_email.delay(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status != 'pending':
            return Response({'error': 'Booking cannot be confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'confirmed'
        booking.save()
        return Response({'status': 'confirmed'})