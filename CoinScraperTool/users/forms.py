from django.contrib.auth.forms import PasswordResetForm
from django.template import loader
from django.conf import settings
from .tasks import send_password_reset_email


# ✅ Overriding the default password reset form
class AsyncPasswordResetForm(PasswordResetForm):

    """
    Using celery to handle the password reset functionality including async email notifcation
    """

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())

        send_password_reset_email.delay(
            subject,
            from_email,
            to_email,
            context,
            html_email_template_name or "emails/password_reset_email.html",
            text_template=email_template_name or "emails/password_reset_email.html"
        )
