from django.shortcuts import render

def my_profile(request):
    context = {'hide_footer': True}
    return render(request, 'user_profile/page-my-profile.html', context=context)