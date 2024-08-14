from django import forms
from phonenumber_field.formfields import PhoneNumberField

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=False)
    subject = forms.CharField(max_length=500, required=True)
    message = forms.CharField(required=True)
    


