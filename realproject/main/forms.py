# Basic
from django import forms
from django.contrib.auth.password_validation import validate_password
# From this app
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



# For the admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'service', 'service_provider', 'country')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'service', 'service_provider', 'country', 'is_active', 'is_staff')


# Registration (Not for the agent!)
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat Password')

    class Meta:
        model = CustomUser
        fields = ['email', 'service', 'service_provider']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('The email field is required.')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email
    
    def clean_service_provider(self):
        cd = self.cleaned_data
        service_provider = cd.get('service_provider', '')
        service = cd.get('service')

        if service:
            if service != 'US' and service_provider == None:
                raise forms.ValidationError('Service provider field can not be empty.')
            if service == 'US':
                return None

        return service_provider
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        #Validating the passwords
        if password:
            validate_password(password)
        else:
            raise forms.ValidationError('The passwords are invalid.')
        
        # Example of non-field validation: Passwords must match
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match.')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user