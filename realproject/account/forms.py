# Basic
from django import forms
from django.contrib.auth.password_validation import validate_password
# From this app
from main.models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from main.models import CustomUser

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
    

# Login with the email
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField()
    remember_me = forms.BooleanField(required=False)

    def confirm_login_allowed(self, user):
        """
        Override this method to customize login validation.
        """
        super().confirm_login_allowed(user)