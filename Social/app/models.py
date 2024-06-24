from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Deferrable, UniqueConstraint, FileField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from os.path import splitext
# Create your models here.

def email_check(value):
    if "@brainvire.com" in value:
        return value
    else:
        raise ValidationError("Brainvire email is required")
    
def valid_image(value):
    ext = splitext(value.name)[1]
    if ext not in settings.CONTENT_TYPES:
        raise ValidationError("Upload valid file with correct extention")
    elif value.size > int(settings.MAX_UPLOAD_SIZE):
        raise ValidationError(f'Please keep filesize under {filesizeformat(settings.MAX_UPLOAD_SIZE)} Current filesize {filesizeformat(value.size)}')
    else:
        return value

def max_image_size(value):
    if value.size > int(settings.MAX_UPLOAD_SIZE):
        raise ValidationError(f'Please keep filesize under {filesizeformat(settings.MAX_UPLOAD_SIZE)} Current filesize {filesizeformat(value.size)}')
    else:
        return value
class CustomUser(AbstractUser):
    first_name=models.CharField(max_length=150,null=True, blank=True)
    last_name=models.CharField(max_length=150,null=True, blank=True)
    email=models.EmailField(null=True, blank=True, validators=[email_check])
    mobile=PhoneNumberField(null=True, blank=True)
    
class Post(models.Model):
    title = models.CharField(max_length=150)
    # image = models.FileField(upload_to='Image', null=True, blank=True, validators=[valid_image])
    image = models.FileField(upload_to='Image', null=True, blank=True, 
                             validators=[FileExtensionValidator(allowed_extensions=["pdf", "jpeg", "png"]), 
                                         max_image_size])
    caption = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=150)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_related', related_query_name='user_related', null=True, blank=True)
    
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
        