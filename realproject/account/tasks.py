from celery import shared_task
import random
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_to_email(verification_code, to_email):
    subject = 'Verify your email'
    from_email = settings.EMAIL_HOST_USER
    text_content = f'Your verification code is {verification_code}'
    html_content = render_to_string('account/verification_email.html', {
        'verification_code': str(verification_code),
    })
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return 'Verification email sent successfully'