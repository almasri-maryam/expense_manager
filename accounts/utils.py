import random

def generate_code():
    return str(random.randint(100000, 999999))

from django.core.mail import send_mail

def send_verification_email(email, code):
    subject = 'رمز التحقق من حسابك'
    message = f'مرحبًا!\nرمز التحقق الخاص بك هو: {code}'
    send_mail(subject, message, None, [email])
