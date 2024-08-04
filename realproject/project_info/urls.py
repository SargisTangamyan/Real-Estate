from django.urls import path
from . import views

app_name = "project_info"

urlpatterns = [
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_conditions')
]
