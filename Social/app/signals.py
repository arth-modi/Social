from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment
from django.core.mail import EmailMessage
from django.conf import settings
from app.task import like_send_mail, comment_send_mail

@receiver(post_save, sender=Like)
def like_post_save(sender, instance, created, **kwargs):
    if created:
        user_email = str(instance.user.email)
        post_title = str(instance.post.title)
        post_user = str(instance.post.user)
        print(user_email, post_title, post_user)
        like_send_mail.delay(user_email, post_title, post_user)
        # subject = "Post Liked"
        # message = f"You liked a post with title - {post.title} and uploaded by {post.user}"
        # sendermail = settings.EMAIL_HOST_USER
        # reciever_email = [user.email]
        # print(reciever_email, message)
        # email = EmailMessage(subject, message, sendermail, reciever_email)
        # email.send()

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    if created:
        user_email = str(instance.user.email)
        user = str(instance.user)
        post = str(instance.post)
        post_title = str(instance.post.title)
        post_user = str(instance.post.user)
        post_user_email = str(instance.post.user.email)
        text = str(instance.text)
        comment_send_mail.delay(user, post, user_email, post_title, post_user, post_user_email, text)
        # subject = f"Commented on Post \"{post}\""
        # message = f"You Commented - \"{instance.text}\" on a post with title - \"{post.title}\" and uploaded by {post.user}"
        # message2 = f"{user} commented - \"{instance.text}\" on your post with title - \"{post.title}\"."
        # sendermail = settings.EMAIL_HOST_USER
        # reciever_email = [user.email]
        # reciever_email2 = [post.user.email]
        # print(reciever_email, message)
        # email = EmailMessage(subject, message, sendermail, reciever_email)
        # email2 = EmailMessage(subject, message2, sendermail, reciever_email2)
        # email.send()
        # email2.send()
        
# post_save.connect(like_post_save, sender=Like)
