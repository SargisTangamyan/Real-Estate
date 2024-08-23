from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

# From the main
from main.models import CompanyProfile

class CompanyForm(forms.ModelForm):
    country = CountryField(blank_label="Select a country").formfield()

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
            if field_name not in ['photo', 'additional_documents']:
                if field_name in ['name', 'first_name', 'last_name']:
                    field.widget.attrs.update({'oninput': 'generateUsername()'})
                field.widget.attrs.update({'class': 'form-control'})