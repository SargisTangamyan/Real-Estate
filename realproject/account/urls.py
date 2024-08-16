from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('waiting/', views.waiting, name='waiting'),
    path('current-time/', views.current_time, name='current_time'),
    path('clear-session/', views.clear_session, name='clear_session'),
    path('verification-success/', views.verification_success, name='verification_success'),
    path('verification-failed/', views.verification_failed, name='verification_failed'),
    path('start_verification/', views.start_verification, name='start_verification'),
    path('validate_registration/', views.validate_registration, name='validate_registration'),
    path('login/', views.login_by_email, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
     # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
