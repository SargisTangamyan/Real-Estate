from user_profile.views import get_model
def registration_info(request):
        SERVICE_CHOICES = (
        ('', 'Select'),
        ('SE', 'Seller'),
        ('RE', 'Renter'),
        ('SAR', 'Seller And Renter')
        )

        SERVICE_PROVIDER_CHOICES = (
            ('', 'Select'),
            ('US', 'User'),
            ('CY', 'Company'),
            ('PE', 'Private Entrepreneur'),
        )

        return {
                'services': SERVICE_CHOICES, 
                'service_providers': SERVICE_PROVIDER_CHOICES
        }



def user_info(request):
        if request.user.is_authenticated:
                model_base = get_model(request.user)
        else:
                return {'user_photo':None}
        try:
                user_info = model_base.objects.get(user=request.user)
                user_photo = user_info.photo.url
        except model_base.DoesNotExist:
                user_photo = None
        return {'user_photo':user_photo}