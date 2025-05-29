from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from api.serializers import (
    ProfileSerializer,
    ScrapeLogSerializer,
    UserPreferenceSerializer,
    ScheduleScrapeSerializer,
    ErrorLogSerializer,
    ExchangeRateSnapshotSerializer,
    CoinComparisonSerializer,
    UserActivitySerializer
)
from scraper_app.models import (
    Profile,
    ScrapeLog,
    UserPreference,
    ScheduledScrape,
    ErrorLog,
    ExchangeRateSnapshot,
    CoinComparison,
    UserActivity
)


# ✅ Viewset for managing user profiles
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filtered_fields = ['username', 'bio']

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_permissions(self):
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Fetching user's profile
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ✅ Viewset for managing scrape logs
class ScrapeLogViewset(ModelViewSet):
    serializer_class = ScrapeLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DjangoFilterBackend
    filtered_fields = ['coin', 'price', 'currency']
    search_fields = ['coin']
    ordering_fields = ['timestamp', 'price']
    ordering = ['-timestamp']

    def get_queryset(self):
        return ScrapeLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # fetching scrape logs filtered by specific coin
    @action(detail=False, methods=['get'])
    def by_coin(self, request):
        coin = request.query_params.get('coin')
        if not coin:
            return Response(
                {'error': 'Coin parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        logs = self.get_queryset().filter(coin__iexact=coin)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    # Fetching price history for a specific coin over time
    @action(detail=False, methods=['get'])
    def price_history(self, request):
        coin = request.query_params.get('coin')
        days = int(request.query_params.get('days', 30))

        if not coin:
            return Response(
                {'error': 'Coin Parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        start_date = timezone.now() - timedelta(days=days)
        logs = self.get_queryset().filter(
            coin__iexact=coin,
            timestamp__gte=start_date
        ).order_by('timestamp')

        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
