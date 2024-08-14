from django.urls import path
from . import views

app_name = "project_info"

urlpatterns = [
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_conditions'),
    path('contact-us/', views.contact_us, name='contact')
]
