# Generated by Django 5.1.3 on 2024-11-26 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YourArea', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
    ]
