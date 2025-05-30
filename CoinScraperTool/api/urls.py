from django.urls import path
from rest_framework_nested import routers
from .views import (
    ProfileViewSet,
    ScrapeLogViewset,
    UserPreferenceViewset,
)
from .import views

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('scrapelogs', ScrapeLogViewset, basename='scrapelog')
router.register('userpreference', UserPreferenceViewset,
                basename='userpreference')

urlpatterns = router.urls
