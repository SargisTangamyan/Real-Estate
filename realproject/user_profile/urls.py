from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'user_profile'

urlpatterns = [
    path('my-profile/', views.my_profile, name='my_profile'),
]
