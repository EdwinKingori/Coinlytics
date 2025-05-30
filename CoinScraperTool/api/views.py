from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Max
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


# ✅ Viewset for managing user's preference
class UserPreferenceViewset(ModelViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DjangoFilterBackend
    filter_fields = ['favorite_coins', 'preferred_currency']
    search_fields = ['preferred_currency', 'favorite_coins']

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # Fetching the user preference
    @action(detail=False, methods=['get'])
    def my_preference(self, request):
        try:
            preference = UserPreference.objects.get(user=request.user)
            serializer = self.get_serializer(preference)
            return Response(serializer)
        except UserPreference.DoesNotExist:
            return Response(
                {'error', 'Preference not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    # Adding a coin to a user's favorites
    @action(detail=True, methods=['post'])
    def get_coin(self, request, pk=None):
        preference = self.get_object()
        coin = request.data.get('coin')

        if not coin:
            return Response(
                {'error': 'Coin parameter is required'},
                status=status.HTTP_404_NOT_FOUND
            )

        if coin not in preference.favorite_coins:
            preference.favorite_coins.append(coin.upper())
            preference.save()

        serializer = self.get_serializer(preference)
        return Response(serializer.data)

    # Removing a coin from a users favorites
    @action(detail=True, methods=['post'])
    def remove_favorite_coin(self, request, pk=None):
        preference = self.get_object()
        coin = request.data.get('coin')

        if not coin:
            return Response(
                {'error': 'Coin parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if coin.upper() in preference.favorite_coins:
            preference.favorite_coins.remove(coin.upper())
            preference.save()

        serializer = self.get_serializer(preference)
        return Response(serializer.data)


# ✅ Viewset to manage scheduled scraping jobs
class ScheduledScrapeViewset(ModelViewSet):
    serializer_class = ScheduleScrapeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DjangoFilterBackend
    filter_fields = ['coin', 'currency', 'is_active']
    ordering_fields = ['last_run', 'interval_minutes']
    ordering = ['-last_run']

    def get_queryset(self):
        return ScheduledScrape.objects.get(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # Toggle the active status of a scheduled scrape
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        Scheduled_scrape = self.get_object()
        Scheduled_scrape.is_active = not Scheduled_scrape.is_active
        Scheduled_scrape.save()

        serializer = self.get_serializer(Scheduled_scrape)
        return Response(serializer.data)

    # Fetching all active scheduled scrapes
    @action(detail=False, methods=['get'])
    def active_scrapes(self, request):
        active_scrapes = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_scrapes, many=True)
        return Response(serializer.data)

    # Updating the last run timestamp for a scheduled scrape
    @action(detail=True, methods=['post'])
    def update_last_run(self, request, pk=None):
        scheduled_scrape = self.get_object()
        scheduled_scrape.last_run = timezone.now()
        scheduled_scrape.save()

        serializer = self.get_serializer(scheduled_scrape)
        return Response(serializer.data)


# ✅ A read-only viewset for error logs with filtering capabilities
class ErrorLogViewset(ModelViewSet):
    serializer_class = ErrorLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DjangoFilterBackend
    search_fields = ['error_message', 'source']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    # Admin users can see all errors, regular users see only their own
    def get_queryset(self):
        if self.request.user.is_staff:
            return ErrorLog.objects.all()
        return ErrorLog.objects.filter(user=self.request.user)

    # Fetching recent errors (last 24 hours)
    @action(detail=False, methods=['get'])
    def recent_errors(self, request):
        yesterday = timezone.now() - timedelta(days=1)
        recent_errors = self.get_queryset().filter(timestamp__gte=yesterday)
        serializer = self.get_serializer(recent_errors, many=True)
        return Response(serializer.data)

    # Fetching error summary by source
    @action(detail=False, methods=['get'])
    def error_summary(self, request):
        from django.db.models import Count

        summary = self.get_queryset().values('source').annotate(
            error_count=Count('id')
        ).order_by('-error_count')


# ✅ Read-only viewset for exchange rate snapshots
class ExchangeRateSnapShotViewset(ModelViewSet):
    serializer_class = ExchangeRateSnapshotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DjangoFilterBackend
    filter_fields = ['base_currency', 'target_currency']
    ordering = ['rate', 'timestamp']

    def get_queryset(self):
        return ExchangeRateSnapshot.objects.all()

    @action(detail=False, methods=['get'])
    def latest_rates(self, request):
        # fetching the latest timestamp for each currency pair
        latest_snapshots = ExchangeRateSnapshot.objects.values(
            'base_currency', 'target_currency'
        ).annotate(
            latest_timestamp=Max('timestamp')
        )

        # Filtering to get only the latest snapshots
        latest_rates = []
        for snapshot_info in latest_snapshots:
            latest_rate = ExchangeRateSnapshot.objects.filter(
                base_currency=snapshot_info['base_currency'],
                target_currency=snapshot_info['target_currency'],
                timestamp=snapshot_info['latest_timestamp']
            ).first()
            if latest_rate:
                latest_rates.append(latest_rate)

        serializer = self.get_serializer(latest_rates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def currency_pair(self, request):
        """Get exchange rate history for specific currency pair"""
        base = request.query_params.get('base')
        target = request.query_params.get('target')
        days = int(request.query_params.get('days', 30))

        if not base or not target:
            return Response(
                {'error': 'Both base and target currency parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = timezone.now() - timedelta(days=days)
        rates = self.get_queryset().filter(
            base_currency=base.upper(),
            target_currency=target.upper(),
            timestamp__gte=start_date
        ).order_by('timestamp')

        serializer = self.get_serializer(rates, many=True)
        return Response(serializer.data)
