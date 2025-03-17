from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class TermsAndConditions(models.Model):
    welcome_text = models.TextField(verbose_name='Welcome Text')
    our_terms = models.TextField(verbose_name='Our Terms')
    conditions = models.TextField(verbose_name='Conditions')
    your_privacy = models.TextField(verbose_name='Your privacy', null=True)
    information_we_collect = models.TextField(verbose_name='Information we collect')

    class Meta:
        verbose_name = "Terms And Conditions"
        verbose_name_plural = "Terms And Conditions"

    def __str__(self) -> str:
        return "Terms And Conditions" 
    
    def save(self, *args, **kwargs):        
        if not self.pk and TermsAndConditions.objects.exists():
            raise ValidationError('There is already an instance of Terms and Conditions.')
        super(TermsAndConditions, self).save(*args, **kwargs)


class ContactUs(models.Model):
    send_email = models.TextField(verbose_name='Send Us An Email')
    contact_us = models.TextField(verbose_name='Contact Us')
    address = models.CharField(verbose_name='Address', max_length=100)
    phone1 = PhoneNumberField(verbose_name='Phone 1', null=True)
    phone2 = PhoneNumberField(verbose_name='Phone 2', null=True, blank=True)
    country = models.CharField(verbose_name='Country', max_length=100, null=True)
    mail = models.EmailField(verbose_name="Mail")
    linkedin = models.CharField(verbose_name="Linkedin", max_length=100, null=True)
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()
    google = models.URLField(null=True)
    pinterest = models.URLField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self) -> str:
        return "Contact Us"

    def save(self, *args, **kwargs):        
        if not self.pk and ContactUs.objects.exists():
            raise ValidationError("There is already an instance of the 'Contact Us'.")
        super(ContactUs, self).save(*args, **kwargs)

