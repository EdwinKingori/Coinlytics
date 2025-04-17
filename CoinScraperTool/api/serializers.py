from rest_framework import serializers
from scraper_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'bio', 'phone_number']
