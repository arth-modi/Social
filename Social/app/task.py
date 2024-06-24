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
    
@shared_task
def like_send_mail(user_email, post_title, post_user):
    subject = "Post Liked"
    message = f"You liked a post with title - {post_title} and uploaded by {post_user}"
    sendermail = settings.EMAIL_HOST_USER
    reciever_email = [user_email]
    print(reciever_email, message)
    email = EmailMessage(subject, message, sendermail, reciever_email)
    email.send()
    
@shared_task
def comment_send_mail(user, post, user_email, post_title, post_user, post_user_email, text):
    subject = f"Commented on Post \"{post}\""
    message = f"You Commented - \"{text}\" on a post with title - \"{post_title}\" and uploaded by {post_user}"
    message2 = f"{user} commented - \"{text}\" on your post with title - \"{post_title}\"."
    sendermail = settings.EMAIL_HOST_USER
    reciever_email = [user_email]
    reciever_email2 = [post_user_email]
    print(reciever_email, message)
    email = EmailMessage(subject, message, sendermail, reciever_email)
    email2 = EmailMessage(subject, message2, sendermail, reciever_email2)
    email.send()
    email2.send()
    
