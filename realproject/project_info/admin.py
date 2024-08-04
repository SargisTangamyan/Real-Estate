from django.contrib import admin
from django.http import HttpRequest
from .models import TermsAndConditions
from django.core.exceptions import ValidationError

class TermsAndConditionsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        if TermsAndConditions.objects.exists():
            return False
        return True
    
    def save_model(self, request, obj, form, change):
        if not change and TermsAndConditions.objects.exists():
            raise ValidationError('There is already an instance of Terms and Conditions.')
        super().save_model(request, obj, form, change)

admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)