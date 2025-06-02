from django.urls import path
from rest_framework_nested import routers
from .views import (
    ProfileViewSet,
    ScrapeLogViewSet,
    UserPreferenceViewSet,
    ScheduledScrapeViewSet,
    ErrorLogViewSet,
    ExchangeRateSnapShotViewSet,
    CoinComparisonViewSet,
    UserActivityViewSet
)
from .import views

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('scrape-logs', ScrapeLogViewSet, basename='scrapelog')
router.register('preferences', UserPreferenceViewSet,
                basename='userpreference')
router.register('schedule-scrapes', ScheduledScrapeViewSet,
                basename='schedulescrape')
router.register('error-logs', ErrorLogViewSet,
                basename='errorlog')
router.register('exchange-rates', ExchangeRateSnapShotViewSet,
                basename='exchangerate')
router.register('coin-comparisons', CoinComparisonViewSet,
                basename='coincomparison')
router.register('user-activities', UserActivityViewSet,
                basename='useractivity')


urlpatterns = router.urls
