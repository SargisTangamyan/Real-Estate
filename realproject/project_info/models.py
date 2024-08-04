from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError

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
