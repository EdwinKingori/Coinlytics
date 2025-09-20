from django.db import models
from django.contrib.auth.models import AbstractUser
from scraper_app.models import Profile

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    @property
    def profile(self):
        profile, created = Profile.objects.get_or_create(user=self)
        return profile
