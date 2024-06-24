from celery import shared_task
# from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from celery.utils.log import get_task_logger
from .models import CustomUser

logger = get_task_logger(__name__)

@shared_task
def sample_task():
    logger.info("The sample task just ran.")
    print("The sample task just ran.")
    

@shared_task
def send_email(firstname, recievermail):
    subject = "Welcome to Social Media App"
    message = f"Hi {firstname}, thank you for registering in Social Media App."
    sendermail = settings.EMAIL_HOST_USER
    email = EmailMessage(subject, message, sendermail, [recievermail])
    email.send()

@shared_task
def send_mail_beat():
    subject = "Welcome to Social Media App"
    message = "Thank you for registering in Social Media App."
    sendermail = settings.EMAIL_HOST_USER
    reciever_email = list(CustomUser.objects.values_list('email', flat=True))
    email = EmailMessage(subject, message, sendermail, reciever_email)
    email.send()
