from django.urls import path
from . import views


app_name = 'homepage'

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('validate_registration/', views.validate_registration, name='validate_registration'),
    path('login/', views.login_by_email, name='login'),
    path('register/', views.register, name='register'),
]
