# Generated by Django 4.2 on 2025-01-29 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_editablecontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editablecontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='editablecontent',
            name='element_id',
        ),
        migrations.AddField(
            model_name='editablecontent',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='editablecontent',
            name='subtitle',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='editablecontent',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
