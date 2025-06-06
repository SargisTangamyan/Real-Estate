# Basic
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import datetime
from django.utils.timezone import now
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
import random

# From the main
from main.models import CustomUser

# from this app
from .forms import RegistrationForm, EmailLoginForm

# From tasks
from .tasks import send_to_email


def send_verification(request, user_data=None):
    if not user_data:
        request.session['verification_time'] = now().isoformat()
    verification_code = random.randint(100000, 999999)
    request.session['verification_code'] = verification_code
    request.session.set_expiry(30 * 60)
    to_email = request.session['email']
    send_to_email.delay(verification_code, to_email)
    

@csrf_exempt
def validate_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})


# Registering the user in the base.html
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
            request.session.set_expiry(86400)  # 1 day in seconds
            send_verification(request, user_data)
            return JsonResponse({'success': True})  # Redirect to a page of your choice
        else:
            # Form is invalid, re-render the form with errors
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = RegistrationForm()
        return HttpResponse("Something went wrong!")


# Logging the user in in the base.html
@csrf_exempt  # Only use this if you have other CSRF protection in place, not recommended for production
def login_by_email(request):
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get('remember_me', False)
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


#Logging out in the base.html
def logout_user(request):
    logout(request)
    return render(request, 'account/logged_out.html', {})


VERIFICATION_EXPIRATION_MINUTES = 15

# After filling the registration the user is moved here to fill the verification code for the email
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
                    return HttpResponseRedirect(reverse('verification_success'))
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


# Giving the current time in js
def current_time(request):
    verification_start_time = request.session.get('verification_time')
    if verification_start_time:
        verification_start_time = datetime.datetime.fromisoformat(verification_start_time)
        expiration_time = verification_start_time + datetime.timedelta(minutes=VERIFICATION_EXPIRATION_MINUTES)
        remaining_time = max(0, (expiration_time - now()).total_seconds())
    else:
        remaining_time = VERIFICATION_EXPIRATION_MINUTES * 60  # Default timer duration if not set
    return JsonResponse({'remaining_time': remaining_time})
    

# After the resend button the timer is restarted and the email is resend
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


def clear_session(request):
    if request.session.get('user_data'):
        del request.session['user_data']
        del request.session['email']
        del request.session['verification_code']
        del request.session['verification_time']
        print('----------cleared the sessions from the clear_session')
    return redirect('homepage:homepage')


# Login from a separate page
def login_page(request):
    if request.user.is_authenticated:
        return redirect('homepage:homepage')
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        # Get the 'next' parameter from the URL
        next_url = request.POST.get('next', request.GET.get('next', None))

        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get('remember_me', False)
            login(request, user)

            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0) # The user will be logged out when the browser is closed
                
            return HttpResponseRedirect(next_url) if next_url else redirect('homepage:homepage')
        else:
            print(form.errors)
            return render(request, 'account/page-login.html', {'error': True, 'form':form, 'next': next_url})
    else:
        form = EmailLoginForm()
    return render(request, 'account/page-login.html', {'next': request.GET.get('next', '')})


# Regiser from a seperate page
def register_page(request):
    if request.user.is_authenticated:
        return redirect('homepage:homepage')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            email = user_data['email']
            request.session['user_data'] = user_data
            request.session['email'] = email
            request.session['verification_time'] = now().isoformat()
            request.session.set_expiry(86400)  # 1 day in seconds
            send_verification(request, user_data)
            return redirect('waiting')
        else:
            # Form is invalid, re-render the form with errors
            print(form.errors)
            return render(request, 'account/page-register.html', {'form': form})
    
    form = RegistrationForm()
    return render(request, 'account/page-register.html', {})