from django.core.mail import EmailMessage
from Sentinel import settings


def send_email(response_data):
    for data in response_data:
        path_parts = data["identity"].split("/")
        criminal_name_parts= path_parts[-2].split("_")
        criminal_name = ' '.join([part.capitalize() for part in criminal_name_parts])
        
        if data['verified']:
            print(data["identity"])

            subject = 'Criminal Recognized'
            message = f"A face has been recognized: {criminal_name} from Lorem ipsum checkpoint"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach_file(data['identity'], 'image/png')
   
            email.send()

            break
 