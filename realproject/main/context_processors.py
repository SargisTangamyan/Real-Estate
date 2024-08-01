def registration_info(request):
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

        return {
                'services': SERVICE_CHOICES, 
                'service_providers': SERVICE_PROVIDER_CHOICES
        }