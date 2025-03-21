# From this app
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



# For the admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'service', 'service_provider')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'service', 'service_provider', 'is_active', 'is_staff')




        

    