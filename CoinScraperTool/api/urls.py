from django.urls import path
from rest_framework_nested import routers
from .views import ProfileViewSet
from .import views

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')

urlpatterns = router.urls
