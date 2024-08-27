from django.shortcuts import render

# From the application
from .forms import CompanyForm, UserForm

# From main
from main.models import CustomUser, CompanyProfile, AgentProfile, PrivateEntrepreneurProfile, SimpleUserProfile



# Finding the user's model and form
USER_TYPES = {
    'CY': {'model': CompanyProfile, 'form': CompanyForm},
    'AG': {'model': AgentProfile, 'form': None},
    'PE': {'model': PrivateEntrepreneurProfile, 'form': None},
    'US': {'model': SimpleUserProfile, 'form': UserForm},
}

def get_model(user):
    if user.service_provider:
        user_info = USER_TYPES.get(user.service_provider)
    else:
        user_info = USER_TYPES.get('US')
    if user_info:
        return user_info['model']
    raise ValueError(f"No model found for user type: {user}")

def get_form(user):
    if user.service_provider:
        user_info = USER_TYPES.get(user.service_provider)
    else:
        user_info = USER_TYPES.get('US')
    if user_info:
        return user_info['form']
    raise ValueError(f"No form found for user type: {user}")

# The end 



def my_profile(request):
    model_base = get_model(request.user)
    
    form_class = get_form(request.user)
    

    try:
        user_profile = model_base.objects.get(user=request.user)
    except model_base.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        if 'profile_info' in request.POST:
            # Initialize the form instance with POST data
            form = form_class(request.POST, request.FILES, instance=user_profile) if user_profile else form_class(request.POST, request.FILES)
            
            if form.is_valid():
                created_profile = form.save(commit=False)
                created_profile.user = request.user
                created_profile.save()

                user = CustomUser.objects.get(id=request.user.id)
                if request.user.service_provider == 'CY':
                    user.username = form.cleaned_data['name']
                else:
                    user.username = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                user.save()

                # Optionally add a success message or redirect
            else:
                print(form.errors)
                context = {
                    'hide_footer': True,
                    'form': form.render("user_profile/forms/form-profile.html"),
                    'form_without_rendering': form
                }
                return render(request, 'user_profile/page-my-profile.html', context=context)

        elif 'social_info' in request.POST:
            # Handle social_info logic here
            pass
    else:
        # GET request - create a blank form
        form = form_class(instance=user_profile) if user_profile else form_class()

    file_name = None
    # if user_profile and user_profile.additional_documents:
    #     documents = []
    #     for document in user_profile.additional_documents:
    #         file_name = document.name.split('/')[-1]  # Extract the file name from the path
    #         documents.append(file_name)


    context = {
        'hide_footer': True,
        'form': form.render("user_profile/forms/form-profile.html"),
        'profile_data': user_profile,
    }
    return render(request, 'user_profile/page-my-profile.html', context=context)
