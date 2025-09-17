from django.core.mail import send_mail
from django.conf import settings

def sendMail(email):
    subject = "Welcome To Winners E-Commerce Application"
    body = f'''
            Hello ! This is a welcome message
            Thank you for joining us

            from Winners Dev Team
        '''
    
    send_mail(
    subject,
    body,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)