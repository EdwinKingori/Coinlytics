from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from scraper_app.models import Profile
from .models import CustomUser

# Creating user instance


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

        # Rendering the html content
        html_content = render_to_string("emails/welcome_email.html", {
            "username": instance.username
        })
        # Sending Email notication when user is created
        subject = "Welcome to CoinScraper"
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.email

        msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Saving the related user profile instance when the user instance created
@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, **kwargs):
    instance.profile.save()
