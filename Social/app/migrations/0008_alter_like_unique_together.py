# Generated by Django 4.2.11 on 2024-06-04 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_like_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
    ]