from .models import ContactUs
import phonenumbers
from phonenumbers  import format_number, PhoneNumberFormat

def contact_us_info(request):
    contact_info = ContactUs.objects.first()
    formatted_number1 = contact_info.phone1  # Default to the raw phone number
    try:
        formatted_number2 = contact_info.phone2  # Default to the raw phone number
    except:
        formatted_number2 = None

    if formatted_number1 and contact_info.phone1:
        try:
            # Parse the number
            parsed_number1 = phonenumbers.parse(str(contact_info.phone1), None)  # None or a specific region if known
            if formatted_number2:
                parsed_number2 = phonenumbers.parse(str(contact_info.phone2), None)  # None or a specific region if known

            # Format the number in international format
            formatted_number1 = format_number(parsed_number1, PhoneNumberFormat.INTERNATIONAL)
            if formatted_number2:
                formatted_number2 = format_number(parsed_number2, PhoneNumberFormat.INTERNATIONAL)
        except:
            # Handle invalid phone numbers gracefully
            pass

    return {'contact_info': contact_info, 'phone1': formatted_number1, 'phone2':formatted_number2}