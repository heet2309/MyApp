# Generated by Django 4.2 on 2025-01-24 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_registrationtable_user_alter_registrationtable_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationtable',
            name='user',
        ),
    ]
