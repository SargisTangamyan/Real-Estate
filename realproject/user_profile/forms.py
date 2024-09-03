from django import forms

# From additional packages
from multiupload.fields import MultiFileField
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

# From the main
from main.models import CompanyProfile, SimpleUserProfile, PrivateEntrepreneurProfile, AgentProfile



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

