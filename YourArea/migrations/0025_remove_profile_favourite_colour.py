# Generated by Django 4.1.4 on 2024-12-02 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YourArea', '0024_alter_profile_favourite_colour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favourite_colour',
        ),
    ]
