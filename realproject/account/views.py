# Basic
from django.shortcuts import render, redirect
import datetime
from django.utils.timezone import now
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

                    CustomUser.objects.create_user(email=user_data['email'], password=user_data['password'], service=user_data['service'], service_provider=user_data['service_provider'])

                    del request.session['user_data']
                    del request.session['verification_code']
                    del request.session['verification_time']
                    return render(request, 'verification_success.html', {})
            else:
                return render(request, 'verification_failed.html', {'error': 'Verification code expired.'})
        else:
            return render(request, 'verification_failed.html', {'error': 'Invalid verification attempt.'})

    return render(request, 'account/verification_waiting.html')

    