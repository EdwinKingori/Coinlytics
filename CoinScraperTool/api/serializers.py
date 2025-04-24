from rest_framework import serializers
from users.serializers import UserSerializer
from scraper_app.models import Profile, ScrapeLog, UserPreference, ScheduledScrape, ErrorLog, ExchangeRateSnapshot, CoinComparison, UserActivity


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'bio', 'phone_number']


class ScrapeLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ScrapeLog
        fields = ['id', 'user', 'coin', 'price', 'currency', 'timestamp']


class UserPreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserPreference
        fields = ['id', 'preferred_currency', 'favorite_coins',
                  'notify_on_price_change', 'notify_threshhold']


class ScheduleScrapeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ScheduledScrape
        fields = ['id', 'coin', 'currency',
                  'interval_minutes', 'is_active', 'last_run']


class ErrorLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ErrorLog
        fields = ['id', 'source', 'error_messsage', 'timestamp']


class ExchangeRateSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateSnapshot
        field = ['base_currency', 'target_currency', 'rate', 'timestamp']


class CoinComparisonSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CoinComparison
        fields = ['id', 'coin1', 'coin2', 'coin1_price',
                  'coin2_price', 'comparison_date']


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'action', 'timestamp']
