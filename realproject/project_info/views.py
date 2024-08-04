from django.shortcuts import render, get_object_or_404
from .models import TermsAndConditions
from django.utils.safestring import mark_safe

def terms_and_conditions(request):
    terms_conditions = get_object_or_404(TermsAndConditions, id=1)
    return render(request, 'project_info/terms-conditions.html', {'terms_conditions': terms_conditions})