from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # This handles hashing and storing the password
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Ensure that `is_staff` and `is_superuser` are set to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Create the user with the provided fields
        user = self.create_user(email, password, **extra_fields)
        
        # Assign all permissions to the superuser
        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)
        
        return user



# -------------------------------------------------- Base User --------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    SERVICE_CHOICES = (
        ('', 'Select'),
        ('US', 'User'),
        ('SE', 'Seller'),
        ('RE', 'Renter'),
        ('SAR', 'Seller And Renter')
    )

    SERVICE_PROVIDER_CHOICES = (
        ('', 'Select'),
        ('CY', 'Company'),
        ('PE', 'Private Entrepreneur'),
    )

    COUNTRY_CHOICES = (
        ('', 'Select'),
        ('AR', 'Armenia'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('GB', 'United Kingdom'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IT', 'Italy'),
        ('ES', 'Spain'),
        ('AU', 'Australia'),
        ('CN', 'China'),
        ('JP', 'Japan'),
        ('IN', 'India'),
        ('BR', 'Brazil'),
        ('ZA', 'South Africa'),
        ('RU', 'Russia'),
        ('MX', 'Mexico'),
        ('KR', 'South Korea'),
        ('SG', 'Singapore'),
        ('NZ', 'New Zealand'),
        ('SE', 'Sweden'),
        ('NO', 'Norway'),
        ('FI', 'Finland'),
    )

    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    service_provider = models.CharField(max_length=100, choices=SERVICE_PROVIDER_CHOICES, null=True, blank=True, default='')
    country = models.CharField(max_length=250, choices=COUNTRY_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email 

    class Meta:
        verbose_name = 'BASE USER'
        verbose_name_plural = 'BASE USERS'   



# -------------------------------------------------- Simple User --------------------------------------------------
class SimpleUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user_account/%Y/%m/%d/", blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True)
    
    class Meta:
        verbose_name = 'SIMPLE USER'
        verbose_name_plural = 'SIMPLE USERS' 

# -------------------------------------------------- Company --------------------------------------------------
def company_photo_upload_to(instance, filename):
    company_name = slugify(instance.name)
    return f"companies/{company_name}/company/{filename}"


class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='companies/%Y/%m/%d/', blank=True)
    name = models.CharField(max_length=100, unique=True)
    license_number = models.CharField(max_length=100, blank=True)
    tax_number = models.CharField(max_length=100, blank=True)
    office_number = PhoneNumberField(blank=True)
    fax_number = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    additional_documents = models.FileField(blank=True)

    # Social Media Links
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
   
    class Meta:
        verbose_name = 'COMPANY'
        verbose_name_plural = 'COMPANIES' 

    def __str__(self):
        return self.name


# -------------------------------------------------- Agent --------------------------------------------------
def agent_photo_upload_to(instance, filename):
    company_name = slugify(instance.company)
    return f"companies/{company_name}/agents/{filename}" 

class AgentProfile(models.Model):
    POSITION_CHOICES = [
        ('', 'Select a position'),  # Empty choice
        ('broker_owner', 'Broker/Owner'), # The person who owns the agency and holds a broker’s license.
        ('managing_broker', 'Managing Broker'), # Oversees the day-to-day operations of the agency and ensures compliance with regulations.
        ('real_estate_agent', 'Real Estate Agent'), # Licensed professionals who assist buyers and sellers in real estate transactions.
        ('listing_agent', 'Listing Agent'), # Specializes in listing properties for sale.
        ('buyers_agent', 'Buyer\'s Agent'), # Focuses on helping buyers find and purchase properties
        ('property_manager', 'Property Manager'), # Manages rental properties on behalf of owners.
        ('leasing_agent', 'Leasing Agent'), # Specializes in renting out properties.
        ('commercial_agent', 'Commercial Real Estate Agent'), # Focuses on commercial properties rather than residential.
    ]
    # Account Information
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=agent_photo_upload_to, blank=True, null=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='company_agents', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    office_number = PhoneNumberField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    description = models.TextField(blank=True)
    additional_documents = models.FileField(blank=True)


    # Social Media Links
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)

    class Meta:
        verbose_name = 'AGENT'
        verbose_name_plural = 'AGENTS' 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------------------------------- PrivateEnterpreneur --------------------------------------------------
class PrivateEntrepreneurProfile(models.Model):
    # Account Information
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=agent_photo_upload_to, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True)
    description = models.TextField(blank=True)
    additional_documents = models.FileField(blank=True)

    # Social Media Links
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)

    class Meta:
        verbose_name = 'PRIVATE ENTERPRENEUR'
        verbose_name_plural = 'PRIVATE ENTERPRENEURS' 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
