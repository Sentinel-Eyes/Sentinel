from django.core.mail import EmailMessage
from Sentinel import settings
from app.models import Criminal


def send_email(response_data):
    for data in response_data:
        path_parts = data["identity"].split("/")
        criminal_name_parts = path_parts[-2].split("_")
        criminal_name = ' '.join([part.capitalize()
                                 for part in criminal_name_parts])

        if data['verified']:
            print(data["identity"])

            first_name = criminal_name_parts[0].capitalize()
            middle_name = criminal_name_parts[1].capitalize() if len(
                criminal_name_parts) > 1 else ""
            last_name = criminal_name_parts[-1].capitalize()

            try:
                criminal = Criminal.objects.get(
                    Criminal_Firstname__iexact=first_name,
                    Criminal_Middlename__iexact=middle_name,
                    Criminal_Lastname__iexact=last_name
                )
            except Criminal.DoesNotExist:
                criminal_description = "Criminal description not found"
            else:
                criminal_description = criminal.Criminal_Description

            subject = 'Criminal Recognized'
            message = f"A face has been recognized: {criminal_name} from Lorem ipsum checkpoint" \
                f"\nCrminal Description: {criminal_description}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach_file(data['identity'], 'image/png')

            email.send()

            break
