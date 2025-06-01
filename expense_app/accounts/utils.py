import random
from django.core.mail import send_mail

def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_email(email, code):
    subject = 'Your account verification code'
    message = f'Hello!\nYour verification code is: {code}'
    send_mail(subject, message, None, [email])
