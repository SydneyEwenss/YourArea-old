# Generated by Django 5.1.3 on 2024-11-27 22:32

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YourArea', '0007_alter_comment_options_alter_comment_post_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
