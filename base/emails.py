from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    subject = "Account Verification mail"
    email_from = settings.EMAIL_HOST_USER
    message = f'Click on this link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject, message, email_from, ['s_krangari@me.iitr.ac.in'])