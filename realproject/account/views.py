# Basic
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import datetime
from django.utils.timezone import now
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ValidationError
# From the main
from main.models import CustomUser

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

                    CustomUser.objects.create_user(
                        email=user_data['email'], 
                        password=user_data['password'], 
                        service=user_data['service'], 
                        service_provider=user_data['service_provider']
                    )

                    del request.session['user_data']
                    del request.session['verification_code']
                    del request.session['verification_time']
                    return HttpResponseRedirect(reverse('account:verification_success'))
                else:
                    return JsonResponse({'message': 'Invalid code. Please try again.'}, status=400)
            else:
                return JsonResponse({'message': 'Verification code has expired.'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid input. Please try again.'}, status=400)
    
    # Calculating the remaining time
    verification_start_time = request.session.get('verification_time')
    print(verification_start_time)
    if verification_start_time:
        verification_start_time = datetime.datetime.fromisoformat(verification_start_time)
        expiration_time = verification_start_time + datetime.timedelta(minutes=VERIFICATION_EXPIRATION_MINUTES)
        remaining_time = max(0, (expiration_time - now()).total_seconds())
    else:
        remaining_time = VERIFICATION_EXPIRATION_MINUTES * 60  # Default timer duration if not set
    print(remaining_time)
    return render(request, 'account/verification_waiting.html', {'remaining_time': remaining_time})



def start_verification(request):
    if request.method == 'POST':
        # Store the current time as the start time for the verification
        request.session['verification_time'] = now().isoformat()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)



def verification_success(request):
    return render(request, 'account/verification_success.html', {})



def verification_failed(request):
    
    message = request.GET.get('message', 'Default message if none provided')
    return render(request, 'account/verification_failed.html', {'message': message})
