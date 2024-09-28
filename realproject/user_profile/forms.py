from django import forms
from django.contrib.auth.password_validation import validate_password

# From additional packages
from multiupload.fields import MultiFileField
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

# From the main
from main.models import CompanyProfile, SimpleUserProfile, PrivateEntrepreneurProfile, AgentProfile, Social



class CompanyForm(forms.ModelForm):
    country = CountryField(blank_label="Select a country").formfield()
    files = MultiFileField(max_num=3, max_file_size=1024*1024*5)

    class Meta:
        model = CompanyProfile
        exclude = ['website', 'facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'pinterest',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7,}),
            "country": CountrySelectWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['photo', 'files']:
                if field_name == 'name':
                    field.widget.attrs.update({'oninput': 'generateUsername()'})
                field.widget.attrs.update({'class': 'form-control'})


class UserForm(forms.ModelForm):
    country = CountryField(blank_label="Select a country").formfield()

    class Meta:
        model = SimpleUserProfile
        fields = '__all__'
        widgets = {
            "country": CountrySelectWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'photo':
                if field_name in ['first_name', 'last_name']:
                    field.widget.attrs.update({'oninput': 'generateUsername()'})
                field.widget.attrs.update({'class': 'form-control'})


class PrivateEntrepreneurForm(forms.ModelForm):
    country = CountryField(blank_label="Select a country").formfield()
    files = MultiFileField(max_num=3, max_file_size=1024*1024*5)

    class Meta:
        model = PrivateEntrepreneurProfile
        exclude = ['website', 'facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'pinterest',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7,}),
            "country": CountrySelectWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['photo', 'files']:
                if field_name in ['first_name', 'last_name']:
                    field.widget.attrs.update({'oninput': 'generateUsername()'})
                field.widget.attrs.update({'class': 'form-control'})


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields='__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs if available
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ method
    
    def clean(self):
        cleaned_data = super().clean()

        try:
            profile = self.user.get_profile()
        except Exception as e:
            print(e)
            raise forms.ValidationError('The profile information must be completed first.')

        # Looking whether there is a filled fields in the request
        if not any(cleaned_data.values()):
            raise forms.ValidationError("At least one field must be filled.")
    
        return cleaned_data
    

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(max_length=100)
    new_password1 = forms.CharField(max_length=100, validators=[validate_password])
    new_password2 = forms.CharField(max_length=100, validators=[validate_password])
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.user and current_password:
            if not self.user.check_password(current_password):
                raise forms.ValidationError('The current password is incorrect.')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password1')
        password_confirm = cleaned_data.get('new_password2')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('New passwords do not match.')
        return cleaned_data
    

class DeletePasswordForm(forms.Form):
    password = forms.CharField(max_length=100)