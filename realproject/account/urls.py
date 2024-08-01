from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('waiting/', views.waiting, name='waiting'),
]
