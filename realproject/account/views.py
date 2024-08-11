# Basic
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import datetime
from django.utils.timezone import now
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import random
from django.utils.timezone import now
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

# From the main
from main.models import CustomUser

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


VERIFICATION_EXPIRATION_MINUTES = 15

def waiting(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        verification_code = request.session.get('verification_code')
        verification_time = request.session.get('verification_time')

        if verification_code and verification_time:
            verification_time = datetime.datetime.fromisoformat(verification_time)
            if now() <= verification_time + datetime.timedelta(minutes=VERIFICATION_EXPIRATION_MINUTES):
                if code == str(verification_code):
                    user_data = request.session.get('user_data')

                    user = CustomUser.objects.create_user(
                        email=user_data['email'], 
                        password=user_data['password'], 
                        service=user_data['service'], 
                        service_provider=user_data['service_provider']
                    )

                    del request.session['user_data']
                    del request.session['email']
                    del request.session['verification_code']
                    del request.session['verification_time']
                    login(request, user)
                    return HttpResponseRedirect(reverse('account:verification_success'))
                else:
                    return JsonResponse({'message': 'Invalid code. Only 1 try left.'}, status=400)
            else:
                return JsonResponse({'message': 'Verification code has expired.'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid input. Please try again.'}, status=400)
    
    if request.session.get('verification_code'):
        # Calculating the remaining time
        verification_start_time = request.session.get('verification_time')
        if verification_start_time:
            verification_start_time = datetime.datetime.fromisoformat(verification_start_time)
            expiration_time = verification_start_time + datetime.timedelta(minutes=VERIFICATION_EXPIRATION_MINUTES)
            remaining_time = max(0, (expiration_time - now()).total_seconds())
        else:
            remaining_time = VERIFICATION_EXPIRATION_MINUTES * 60  # Default timer duration if not set
        return render(request, 'account/verification_waiting.html', {'remaining_time': remaining_time})
    return redirect('homepage:homepage')


@csrf_exempt
def start_verification(request):
    if request.method == 'POST':
        send_verification(request)
        # Store the current time as the start time for the verification
        request.session['verification_time'] = now().isoformat() # Can be deleted (The process is taken by the send_verification function)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)



def verification_success(request):
    return render(request, 'account/verification_success.html', {})



def verification_failed(request):
    message = request.GET.get('message', 'Error occurred')
    resendUsed = request.GET.get('resendUsed', False)
    print(resendUsed)
    if resendUsed != 'false':
        del request.session['user_data']
        del request.session['email']
        del request.session['verification_code']
        del request.session['verification_time']
        print('-------cleaned.')
    return render(request, 'account/verification_failed.html', {'message': message, 'resendUsed': resendUsed})
