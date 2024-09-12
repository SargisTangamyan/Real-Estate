from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SimpleUserProfile, CompanyProfile, AgentProfile, PrivateEntrepreneurProfile, Social
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'service', 'service_provider', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('service', 'service_provider', 'username', 'slug', 'profile_status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'service', 'service_provider'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(SimpleUserProfile)
admin.site.register(CompanyProfile)
admin.site.register(AgentProfile)
admin.site.register(PrivateEntrepreneurProfile)
admin.site.register(Social)

