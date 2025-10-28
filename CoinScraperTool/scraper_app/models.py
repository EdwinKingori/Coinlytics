from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=200, unique=True, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ✅ Model to store the scraped coin price logs for future reference or analysis
class ScrapeLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scrape_logs')
    coin = models.CharField(max_length=20)  # eg BTC, ETH
    price = models.DecimalField(max_digits=20, decimal_places=6)
    currency = models.CharField(max_length=10, default='USD')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.coin} price at {self.timestamp}"


# ✅ Model to track the user preference for notifications
class UserPreference(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    # user's preference fiat currency for conversion
    preferred_currency = models.CharField(max_length=20, default='USD')
    # lists favorite coins eg{"BTC", "ETH"}
    favorite_coins = models.JSONField(default=list)
    notify_on_price_change = models.BooleanField(default=True)
    notify_threshhold = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.0)  # Percentage change threshold for notifications

    def __str__(self):
        return f"Preferences for {self.user.username}"


# ✅ Model to schedule scraping jobs based on user preference
class ScheduledScrape(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sheduled_scrapes')
    coin = models.CharField(max_length=20)  # eg BTC, ETH
    currency = models.CharField(max_length=10, default='USD')
    # how often to scrape (e.g., every 60 minutes )
    interval_minutes = models.IntegerField(default=60)
    # Whether the scrappe is active
    is_active = models.BooleanField(default=True)
    # Time of the last successful scrape
    last_run = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.coin} every {self.interval_minutes} mins"


# ✅ Model to store errors or failures that occured during scraping or API interactions
class ErrorLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # e.g. "openExchange or CoinGecko"
    source = models.CharField(max_length=100)
    error_message = models.TextField()  # Description of the error
    timestamp = models.DateTimeField(
        auto_now_add=True)  # When the error occured

    def __str__(self):
        return f"Error at {self.timestamp} from {self.source}"


# ✅ Model to store the exchange rate snapshots used during the scraping process
class ExchangeRateSnapshot(models.Model):
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    # Echange rate (e.g., 0.85)
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    timestamp = models.DateTimeField(
        auto_now_add=True)  # Timestamp of the snapshot

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency} @ {self.rate}"


# ✅ Model to store price comparisons btw different coins
class CoinComparison(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coin_comparisons')
    coin1 = models.CharField(max_length=20)  # eg BTC, ETH
    coin2 = models.CharField(max_length=20)  # eg BTC, ETH
    coin1_price = models.DecimalField(max_digits=20, decimal_places=6)
    coin2_price = models.DecimalField(max_digits=20, decimal_places=6)
    comparison_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison of {self.coin1} and {self.coin2} on {self.comparison_date}"


# ✅ Model to monitor user activity on the platform, which help to provide analytics and insights
class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="activities")
    # Description of the action (e.g., "scraped BTC price")
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
