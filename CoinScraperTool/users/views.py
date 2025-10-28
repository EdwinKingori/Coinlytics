from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from .forms import AsyncPasswordResetForm
# Create your views here.


class CustomPasswordReserView(PasswordResetView):
    form_class = AsyncPasswordResetForm
    template_name = "emails/password_reset_request_page.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    html_email_template_name = "emails/password_reset.html"
