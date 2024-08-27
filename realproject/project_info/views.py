# Basic
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

# From itself
from .models import TermsAndConditions, ContactUs
from .forms import ContactUsForm
from .tasks import contact_send

# From the main
from main.models import CustomUser

def terms_and_conditions(request):
    terms_conditions = get_object_or_404(TermsAndConditions, id=1)
    return render(request, 'project_info/terms-conditions.html', {'terms_conditions': terms_conditions})


def contact_us(request):
    # Fetch the mail address from the ContactUs model
    mail = get_object_or_404(ContactUs).mail
    
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone', None)
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            # Check for authenticated user details
            username = None
            service = None
            service_provider = None
            if request.user.is_authenticated:
                username = request.user.email
                service_provider = request.user.get_service_provider_display()
                if service_provider != 'US':
                    service = request.user.get_service_display()

            # Prepare the email content
            text_content = f'''
            Name: {name}\n
            Email: {email}\n
            Phone: {phone or 'N/A'}\n
            Username: {username or 'Anonymous'}\n
            Service: {service or 'N/A'}\n
            Service Provider: {service_provider or 'N/A'}\n
            Message: {message}
            '''
            
            html_content = render_to_string('project_info/contact_mail.html', {
                'username': username,
                'service': service,
                'service_provider': service_provider,
                'name': name,
                'email': email, 
                'phone': phone,
                'message': message,
            })

            # Send the email
            contact_send.delay(subject, text_content, mail, html_content, email)

            return render(request, 'project_info/page-contact.html', {'success': True})
        else:
            return render(request, 'project_info/page-contact.html', {'form': form})

    # Render the contact page with the form
    return render(request, 'project_info/page-contact.html', {})