# Generated by Django 4.2 on 2025-01-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_alter_editablecontent_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditableContent2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('subtitle', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'editable_content2',
            },
        ),
    ]
