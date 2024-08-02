# Basic 
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import random
from django.utils.timezone import now
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# from this app
from .forms import RegistrationForm

def send_verification(request, user_data=None):
    if user_data:
        request.session['user_data'] = user_data
        request.session['verification_time'] = now().isoformat()
        request.session['user_data'] = user_data
    verification_code = random.randint(100000, 999999)
    request.session['verification_code'] = verification_code
    subject = 'Verify your email'
    from_email = settings.EMAIL_HOST_USER
    to_email = user_data['email']
    text_content = f'Your verification code is {verification_code}'
    html_content = render_to_string('account/verification_email.html', {
        'verification_code': str(verification_code),
    })
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@csrf_exempt
def validate_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            send_verification(request, user_data)
            return JsonResponse({'success': True})  # Redirect to a page of your choice
        else:
            # Form is invalid, re-render the form with errors
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm()
        print(form.errors)
        return HttpResponse("Something went wrong!")



class Homepage(View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'main/index6.html', context=context)
    



    
        
