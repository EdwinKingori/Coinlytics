from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "Coin Scrape Admin"
admin.site.index_title = "Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scraper_app.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('favicon.ico', RedirectView.as_view(
        url='/static/favicon.ico', permanent=True)),
]
