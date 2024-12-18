from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import DetailView
from phonenumbers  import format_number, PhoneNumberFormat
import phonenumbers
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

# From the application
from .forms import CompanyForm, UserForm, PrivateEntrepreneurForm, SocialForm, PasswordChangeForm, DeletePasswordForm

# From main
from main.models import CustomUser, CompanyProfile, AgentProfile, PrivateEntrepreneurProfile, SimpleUserProfile, UploadedFile, Social



# Finding the user's model and form
USER_TYPES = {
    'CY': {'model': CompanyProfile, 'form': CompanyForm},
    'AG': {'model': AgentProfile, 'form': None},
    'PE': {'model': PrivateEntrepreneurProfile, 'form': PrivateEntrepreneurForm},
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


@login_required
def my_profile(request):
    # Getting the model and the form for the user
    model_base = get_model(request.user)    
    form_class = get_form(request.user)
    
    # Trying to retrieve the user's profile information
    try:
        user_profile = model_base.objects.get(user=request.user)
    except model_base.DoesNotExist:
        user_profile = None

    # Trying to get the social information if there is any
    try:
        social = Social.objects.get(user = request.user)
    except Social.DoesNotExist:
        social = None
    
    form_social = SocialForm(instance=social) if social else SocialForm()

    changer_form = None

    # The post request handling
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
                    username = form.cleaned_data['name']
                else:
                    username = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"

                user.username = username
                user.slug = slugify(username)
                user.profile_status = True
                user.save()

                # Saving the files
                if form.cleaned_data.get('files'):
                    uploaded_file_instance = UploadedFile.objects.filter(user=request.user).first()
                    if uploaded_file_instance:
                        uploaded_file_instance.delete_user_files()
                
                    for file in form.cleaned_data['files']:
                        UploadedFile.objects.create(user=request.user, file=file)

                # Optionally add a success message or redirect
            else:
                print(form.errors)
                context = {
                    'hide_footer': True,
                    'form': form.render("user_profile/forms/form-profile.html"),
                    'form_without_rendering': form
                }
                return render(request, 'user_profile/page-my-profile.html', context=context)

        elif 'social' in request.POST:
            form_social = SocialForm(request.POST, user=request.user, instance=social) if social else SocialForm(request.POST, user=request.user)
            if form_social.is_valid():
                form_social_save = form_social.save(commit=False)
                form_social_save.user = request.user
                form_social_save.save()
            else:
                print(form_social.errors)
        
        elif 'change_password' in request.POST:
            changer_form = PasswordChangeForm(request.POST, user=request.user)
            if changer_form.is_valid():
                password_data = changer_form.cleaned_data
                new_password = password_data.get('new_password1')
                user = request.user
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user) # For keeping the user logged in
                messages.success(request, "The password is changed successfully.") 
            else:
                messages.error(request, "Error occurred while trying to change the password.")
                print(changer_form.errors)
            
        elif 'delete_account' in request.POST:
            delete_form = DeletePasswordForm(request.POST)
            if delete_form.is_valid():
                if request.user.check_password(delete_form.cleaned_data['password']):
                    delete_user = request.user
                    delete_user.is_active = False
                    delete_user.save()
                    logout(request)
                    messages.info(request, 'Your account has been deleted')
                    return JsonResponse({'success': True})

                else:
                    # Return a JSON response for incorrect password
                    return JsonResponse({'success': False}, status=400)
            else:
                # Return a JSON response for invalid form submission
                return JsonResponse({'success': False}, status=400) 
   
    form = form_class(instance=user_profile) if user_profile else form_class()

    # Giving the name of the documents if there are any
    documents = None
    if user_profile and request.user.user_documents.exists():
        documents = []
        for document in request.user.user_documents.all():
            file_name = document.file.name.split('/')[-1]  # Extract the file name from the path
            documents.append(file_name)

    context = {
        'hide_footer': True,
        'form': form.render("user_profile/forms/form-profile.html"),
        'form_social':form_social,
        'profile_data': user_profile,
        'documents': documents,
        'changer_form': changer_form,
    }
    return render(request, 'user_profile/page-my-profile.html', context=context)


class Overview(DetailView):
    model = CustomUser
    context_object_name = 'profile_data'
    def get_template_names(self) -> list[str]:
        if self.request.user.service_provider == "CY":
            return ["user_profile/page-listing-agencies-v3.html"]
        else:
            return ["user_profile/page-listing-agent-v3.html"]
        
    def get_object(self) -> Model:
        user = get_object_or_404(CustomUser, id=self.kwargs['pk'], slug=self.kwargs['slug'], profile_status=True)
        return user
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.service_provider in ['CY', 'AG']:
            office_number = phonenumbers.parse(str(self.request.user.get_profile().office_number), None)
            context['office_number'] = format_number(office_number, PhoneNumberFormat.INTERNATIONAL)
        if self.request.user.service_provider in ['AG', 'PE']:
            phone_number = phonenumbers.parse(str(self.request.user.get_profile().phone_number), None)
            context['phone_number'] = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
        return context
        
    
        
    