from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'user_profile'

urlpatterns = [
    path('my-profile/', views.my_profile, name='my_profile'),
    path('overview/<int:pk>/<slug:slug>/', views.Overview.as_view(), name='overview'),
    # path('overview/v1', TemplateView.as_view(template_name = 'user_profile/page-listing-agent-v3.html')),
    # path('overview/v2', TemplateView.as_view(template_name = 'user_profile/page-listing-agencies-v3.html')),
]
