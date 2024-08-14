from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

@shared_task
def contact_send(subject, text_content, mail, html_content, users_email):
    # Message for the admin
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [mail])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Message for the user
    subject = 'Contact Received'
    message = """Hello, \nThank you for reaching out to Synergy Terrace Realty Customer Support!\n
We appreciate you taking the time to contact us, and we are here to assist you with any questions or concerns.\n
Your inquiry has been received, and we'll make sure to get back to you within 72 hours. Our Customer Support team is dedicated to providing the excellent service you deserve, and we will do our best to resolve your issue as soon as possible.\n 
Thank you for your patience and understanding. We are continuously working on improving our product and look forward to your feedback.\n 
This is an automatic reply.\n 
Best regards,\n 
Synergy Terrace Realty Customer Support Team"""
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[users_email,])

    return 'The messages are sent.'


