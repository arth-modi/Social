# Generated by Django 4.2.11 on 2024-05-27 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
    ]