from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('waiting/', views.waiting, name='waiting'),
    path('verification-success/', views.verification_success, name='verification_success'),
    path('verification-failed/', views.verification_failed, name='verification_failed'),
    path('start_verification/', views.start_verification, name='start_verification'),
    path('validate_registration/', views.validate_registration, name='validate_registration'),
    path('login/', views.login_by_email, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
]
