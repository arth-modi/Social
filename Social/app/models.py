from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Deferrable, UniqueConstraint
# from django.contrib.auth.models import User

# Create your models here.

class CustomUser(AbstractUser):
    mobile=PhoneNumberField(null=False, blank=False)
    
class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='Image')
    caption = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=150)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comment', related_query_name='user_comment', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment', related_query_name='post_comment')
    text = models.TextField()

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_like', related_query_name='user_like', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like', related_query_name='post_like')
    
    class Meta:
        unique_together = ('user','post')