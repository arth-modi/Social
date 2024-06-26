# Generated by Django 4.2.11 on 2024-06-20 10:21

import app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[app.models.email_check]),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='Image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'png']), app.models.max_image_size]),
        ),
    ]
