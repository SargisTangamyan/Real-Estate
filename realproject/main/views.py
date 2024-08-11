# Basic 
from django.shortcuts import render
from django.views import View


class Homepage(View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'main/index6.html', context=context)
    



    
        
