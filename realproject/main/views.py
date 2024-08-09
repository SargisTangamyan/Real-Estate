# Basic 
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import random
from django.utils.timezone import now
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout

# from this app
from .forms import RegistrationForm, EmailLoginForm

def send_verification(request, user_data=None):
    if not user_data:
        request.session['verification_time'] = now().isoformat()
    verification_code = random.randint(100000, 999999)
    request.session['verification_code'] = verification_code
    request.session.set_expiry(30 * 60)
    subject = 'Verify your email'
    from_email = settings.EMAIL_HOST_USER
    to_email = request.session['email']
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


# Registering the user
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            email = user_data['email']
            request.session['user_data'] = user_data
            request.session['email'] = email
            request.session['verification_time'] = now().isoformat()
            request.session.set_expiry(30 * 60)  # 30 minutes in seconds
            send_verification(request, user_data)
            return JsonResponse({'success': True})  # Redirect to a page of your choice
        else:
            # Form is invalid, re-render the form with errors
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm()
        print(form.errors)
        return HttpResponse("Something went wrong!")


# Logging the user in 
@csrf_exempt  # Only use this if you have other CSRF protection in place, not recommended for production
def login_by_email(request):
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get('remember_me', False)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
            login(request, user)
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


#Logging out
def logout_user(request):
    logout(request)
    return render(request, 'account/logged_out.html', {})

class Homepage(View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'main/index6.html', context=context)
    



    
        
